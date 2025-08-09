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

        # NO_PROXY 列表（可能包含通配符/本地域标记，简单拼接即可，大多数场景够用）
        $noProxy = $null
        if ($proxy.BypassList -and $proxy.BypassList.Count -gt 0) {
            $noProxy = ($proxy.BypassList -join ",")
        }

        return [PSCustomObject]@{
            UseProxy = $true
            Proxy    = $proxyUri.AbsoluteUri  # 形如 http://proxy:port
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

# 检测系统代理（以 GitHub 为测试地址，能正确触发 PAC/绕过规则）
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

# 用于存储任务的状态
$jobs = @()
$results = @()

# 获取所有包含 .git 文件夹的目录
$repos = Get-ChildItem -Path $root_dir -Directory | Where-Object { Test-Path "$($_.FullName)\.git" }

# 输出总仓库数
Write-Host "找到 $($repos.Count) 个 Git 仓库，开始并行拉取..."

# 准备传递到作业的代理参数
$jobProxy     = if ($proxyInfo.UseProxy) { $proxyInfo.Proxy } else { $null }
$jobNoProxy   = $proxyInfo.NoProxy

# 遍历所有仓库
foreach ($repo in $repos) {
    # 如果当前并行任务数达到最大值，等待任务完成
    while ($jobs.Count -ge $maxParallelJobs) {
        $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
        foreach ($job in $completedJobs) {
            $output = Receive-Job -Job $job
            $results += [PSCustomObject]@{
                Repository = $job.Name
                Status     = if ($job.State -eq "Completed") { "成功" } else { "失败" }
                Output     = $output
            }
            Remove-Job -Job $job
            $jobs = $jobs | Where-Object { $_.Id -ne $job.Id }
        }
        Start-Sleep -Milliseconds 200
    }

    # 启动新任务
    $job = Start-Job -Name $repo.FullName -ScriptBlock {
        param($dir, $proxy, $noProxy)
        # 作业是独立进程，需在作业内部设置环境变量
        if ($proxy) {
            $env:HTTP_PROXY  = $proxy
            $env:HTTPS_PROXY = $proxy
        }
        if ($noProxy) {
            $env:NO_PROXY = $noProxy
        }

        Push-Location $dir
        try {
            # 直接使用 git pull；若需临时指定代理也可改为: git -c http.proxy=$proxy -c https.proxy=$proxy pull
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

    $jobs += $job
    Write-Host "启动任务: $($repo.FullName)"
}

# 等待剩余任务完成
while ($jobs.Count -gt 0) {
    $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
    foreach ($job in $completedJobs) {
        $output = Receive-Job -Job $job
        $results += [PSCustomObject]@{
            Repository = $job.Name
            Status     = if ($job.State -eq "Completed") { "成功" } else { "失败" }
            Output     = $output
        }
        Remove-Job -Job $job
        $jobs = $jobs | Where-Object { $_.Id -ne $job.Id }
    }
    Start-Sleep -Milliseconds 200
}

# 输出最终结果
Write-Host "`n所有任务完成，结果如下："
$results | Format-Table -AutoSize

# 统计成功和失败的任务数
$successCount = ($results | Where-Object { $_.Status -eq "成功" }).Count
$failedCount = ($results | Where-Object { $_.Status -eq "失败" }).Count

Write-Host "成功: $successCount, 失败: $failedCount"