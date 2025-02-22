param (
    [string]$root_dir
)

if (-not $root_dir) {
    Write-Host "���ṩһ��·����Ϊ����"
    exit 1
}

if (-not (Test-Path $root_dir)) {
    Write-Host "·��������: $root_dir"
    exit 1
}

# �����������
$maxParallelJobs = 4

# ���ڴ洢�����״̬
$jobs = @()
$results = @()

# ��ȡ���а��� .git �ļ��е�Ŀ¼
$repos = Get-ChildItem -Path $root_dir -Directory | Where-Object { Test-Path "$($_.FullName)\.git" }

# ����ֿܲ���
Write-Host "�ҵ� $($repos.Count) �� Git �ֿ⣬��ʼ������ȡ..."

# �������вֿ�
foreach ($repo in $repos) {
    # �����ǰ�����������ﵽ���ֵ���ȴ��������
    while ($jobs.Count -ge $maxParallelJobs) {
        $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
        foreach ($job in $completedJobs) {
            $output = Receive-Job -Job $job
            $results += [PSCustomObject]@{
                Repository = $job.Name
                Status    = if ($job.State -eq "Completed") { "�ɹ�" } else { "ʧ��" }
                Output     = $output
            }
            Remove-Job -Job $job
            $jobs = $jobs | Where-Object { $_.Id -ne $job.Id }
        }
        Start-Sleep -Milliseconds 200
    }

    # ����������
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
    Write-Host "��������: $($repo.FullName)"
}

# �ȴ�ʣ���������
while ($jobs.Count -gt 0) {
    $completedJobs = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
    foreach ($job in $completedJobs) {
        $output = Receive-Job -Job $job
        $results += [PSCustomObject]@{
            Repository = $job.Name
            Status    = if ($job.State -eq "Completed") { "�ɹ�" } else { "ʧ��" }
            Output     = $output
        }
        Remove-Job -Job $job
        $jobs = $jobs | Where-Object { $_.Id -ne $job.Id }
    }
    Start-Sleep -Milliseconds 200
}

# ������ս��
Write-Host "`n����������ɣ�������£�"
$results | Format-Table -AutoSize

# ͳ�Ƴɹ���ʧ�ܵ�������
$successCount = ($results | Where-Object { $_.Status -eq "�ɹ�" }).Count
$failedCount = ($results | Where-Object { $_.Status -eq "ʧ��" }).Count

Write-Host "�ɹ�: $successCount, ʧ��: $failedCount"