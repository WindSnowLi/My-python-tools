param (
    [string]$root_dir
)

if (-not $root_dir) {
    Write-Host "请提供一个路径作为参数"
    exit 1
}

if (-not (Test-Path $root_dir)) {
    Write-Host "路径不存在: $root_dir"
    exit 1
}

function Get-SystemProxyInfo {
    param(
        [Parameter(Mandatory)]
        [string]$TestUrl
    )
    try {
        $proxy = [System.Net.WebRequest]::DefaultWebProxy
        if (-not $proxy) {
            return [PSCustomObject]@{
                UseProxy = $false
                Proxy    = $null
                NoProxy  = $null
            }
        }

        $uri = [Uri]$TestUrl
        if ($proxy.IsBypassed($uri)) {
            return [PSCustomObject]@{
                UseProxy = $false
                Proxy    = $null
                NoProxy  = ($proxy.BypassList -join ",")
            }
        }

        $proxyUri = $proxy.GetProxy($uri)

        $noProxy = $null
        if ($proxy.BypassList -and $proxy.BypassList.Count -gt 0) {
            $noProxy = ($proxy.BypassList -join ",")
        }

        return [PSCustomObject]@{
            UseProxy = $true
            Proxy    = $proxyUri.AbsoluteUri
            NoProxy  = $noProxy
        }
    } catch {
        Write-Host "检测系统代理失败：$($_.Exception.Message)"
        return [PSCustomObject]@{
            UseProxy = $false
            Proxy    = $null
            NoProxy  = $null
        }
    }
}

# 检测系统代理
$proxyInfo = Get-SystemProxyInfo -TestUrl "https://github.com"
if ($proxyInfo.UseProxy -and $proxyInfo.Proxy) {
    Write-Host "检测到系统代理: $($proxyInfo.Proxy)"
    if ($proxyInfo.NoProxy) {
        Write-Host "NO_PROXY: $($proxyInfo.NoProxy)"
    }
} else {
    Write-Host "未检测到需要代理，直接连接。"
}

# 最大并行任务数
$maxParallelJobs = 4

# 用于存储任务的状态（使用 ArrayList 更稳妥）
$jobs    = [System.Collections.ArrayList]::new()
$results = [System.Collections.ArrayList]::new()

# 获取所有包含 .git 文件夹的目录
$repos = Get-ChildItem -Path $root_dir -Directory | Where-Object { Test-Path "$($_.FullName)\.git" }

Write-Host "找到 $($repos.Count) 个 Git 仓库，开始并行拉取..."

# 准备传递到作业的代理参数
$jobProxy   = if ($proxyInfo.UseProxy) { $proxyInfo.Proxy } else { $null }
$jobNoProxy = $proxyInfo.NoProxy

foreach ($repo in $repos) {
    # 控制并发度
    while ($jobs.Count -ge $maxParallelJobs) {
        $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
        foreach ($jobItem in $completedJobs) {
            $output = Receive-Job -Job $jobItem
            $null = $results.Add([PSCustomObject]@{
                Repository = $jobItem.Name
                Status     = if ($jobItem.State -eq "Completed") { "成功" } else { "失败" }
                Output     = $output
            })
            Remove-Job -Job $jobItem
            [void]$jobs.Remove($jobItem)
        }
        Start-Sleep -Milliseconds 200
    }

    # 启动新任务
    $job = Start-Job -Name $repo.FullName -ScriptBlock {
        param($dir, $proxy, $noProxy)
        if ($proxy) {
            $env:HTTP_PROXY  = $proxy
            $env:HTTPS_PROXY = $proxy
        }
        if ($noProxy) {
            $env:NO_PROXY = $noProxy
        }

        Push-Location $dir
        try {
            $output = git pull 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw $output
            }
            $output
        } catch {
            throw $_
        } finally {
            Pop-Location
        }
    } -ArgumentList $repo.FullName, $jobProxy, $jobNoProxy

    $null = $jobs.Add($job)
    Write-Host "启动任务: $($repo.FullName)"
}

# 等待剩余任务完成
while ($jobs.Count -gt 0) {
    $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
    foreach ($jobItem in $completedJobs) {
        $output = Receive-Job -Job $jobItem
        $null = $results.Add([PSCustomObject]@{
            Repository = $jobItem.Name
            Status     = if ($jobItem.State -eq "Completed") { "成功" } else { "失败" }
            Output     = $output
        })
        Remove-Job -Job $jobItem
        [void]$jobs.Remove($jobItem)
    }
    Start-Sleep -Milliseconds 200
}

Write-Host "`n所有任务完成，结果如下："
$results | Format-Table -AutoSize

$successCount = ($results | Where-Object { $_.Status -eq "成功" }).Count
$failedCount  = ($results | Where-Object { $_.Status -eq "失败" }).Count
Write-Host "成功: $successCount, 失败: $failedCount"