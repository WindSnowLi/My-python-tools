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

# 最大并行任务数
$maxParallelJobs = 4

# 用于存储任务的状态
$jobs = @()
$results = @()

# 获取所有包含 .git 文件夹的目录
$repos = Get-ChildItem -Path $root_dir -Directory | Where-Object { Test-Path "$($_.FullName)\.git" }

# 输出总仓库数
Write-Host "找到 $($repos.Count) 个 Git 仓库，开始并行拉取..."

# 遍历所有仓库
foreach ($repo in $repos) {
    # 如果当前并行任务数达到最大值，等待任务完成
    while ($jobs.Count -ge $maxParallelJobs) {
        $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
        foreach ($job in $completedJobs) {
            $output = Receive-Job -Job $job
            $results += [PSCustomObject]@{
                Repository = $job.Name
                Status    = if ($job.State -eq "Completed") { "成功" } else { "失败" }
                Output     = $output
            }
            Remove-Job -Job $job
            $jobs = $jobs | Where-Object { $_.Id -ne $job.Id }
        }
        Start-Sleep -Milliseconds 200
    }

    # 启动新任务
    $job = Start-Job -Name $repo.FullName -ScriptBlock {
        param($dir)
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
    } -ArgumentList $repo.FullName

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
            Status    = if ($job.State -eq "Completed") { "成功" } else { "失败" }
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