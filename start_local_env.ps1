# Iniciar o ambiente de desenvolvimento local para o MySword Tools

Write-Host '==================================================' -ForegroundColor Cyan
Write-Host '    MySword Tools - Iniciando Ambiente Local' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan

# Função para verificar se a porta está em uso e agir
function Get-AvailablePort {
    param (
        [int]$targetPort,
        [string]$serviceName
    )

    while ($true) {
        # Busca conexões na porta em estado Listen
        $conn = Get-NetTCPConnection -LocalPort $targetPort -State Listen -ErrorAction SilentlyContinue
        if ($null -eq $conn) {
            return $targetPort
        }

        # Porta ocupada
        $pidNum = $conn[0].OwningProcess
        $procName = (Get-Process -Id $pidNum -ErrorAction SilentlyContinue).Name
        if ($null -eq $procName) { $procName = 'Desconhecido' }

        Write-Host ''
        Write-Host ('⚠️ A porta ' + $targetPort + ' (desejada para o ' + $serviceName + ") está em uso por: '" + $procName + "' (PID: " + $pidNum + ')') -ForegroundColor Yellow
        Write-Host 'Escolha uma ação:' -ForegroundColor Gray
        Write-Host '  [1] Terminar o processo atual (Kill)'
        Write-Host '  [2] Digitar outra porta'
        Write-Host '  [3] Sair'
        
        $opcao = Read-Host 'Digite a opção (1-3)'
        
        if ($opcao -eq '1') {
            Write-Host ('Encerrando processo ' + $procName + ' (PID: ' + $pidNum + ')...') -ForegroundColor Red
            Stop-Process -Id $pidNum -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
        }
        elseif ($opcao -eq '2') {
            $novaPorta = Read-Host 'Digite o novo número de porta'
            if ([int]::TryParse($novaPorta, [ref]$targetPort)) {
                Write-Host ('Verificando a porta ' + $targetPort + '...') -ForegroundColor Gray
            } else {
                Write-Host 'Porta inválida. Mantendo a porta anterior.' -ForegroundColor Red
            }
        }
        else {
            Write-Host 'Saindo...' -ForegroundColor Gray
            exit
        }
    }
}

# 1. Validar e obter portas disponíveis
$backendPort = Get-AvailablePort -targetPort 8000 -serviceName 'Backend (FastAPI)'
$frontendPort = Get-AvailablePort -targetPort 3000 -serviceName 'Frontend (Next.js)'

# 2. Configurar variáveis de ambiente para a sessão atual
$env:STRIPE_SECRET_KEY = 'mock_stripe_secret_key'
$env:STRIPE_WEBHOOK_SECRET = 'whsec_test_webhook_secret_fake'
$env:NEXT_PUBLIC_API_URL = ('http://localhost:' + $backendPort)


# 3. Iniciar o Backend (FastAPI) em uma nova janela do console
Write-Host ('[1/3] Iniciando o Backend FastAPI na porta ' + $backendPort + '...') -ForegroundColor Yellow
$backendCmd = 'cd c:\projects\mysword-tools; .\venv\Scripts\python.exe -m uvicorn src.web.app:app --reload --port ' + $backendPort
Start-Process powershell -ArgumentList '-NoExit', '-Command', $backendCmd -WindowStyle Normal

# 4. Instalar dependências do Frontend (Next.js)
Write-Host '[2/3] Verificando dependências do Frontend Next.js...' -ForegroundColor Yellow
cd c:\projects\mysword-tools\src\web\frontend
npm install

# 5. Iniciar o Frontend (Next.js) em uma nova janela do console passando a porta dinâmica e a URL da API
Write-Host ('[3/3] Iniciando o Frontend Next.js na porta ' + $frontendPort + '...') -ForegroundColor Yellow
$frontendCmd = 'cd c:\projects\mysword-tools\src\web\frontend; $env:NEXT_PUBLIC_API_URL=''http://localhost:' + $backendPort + '''; npx next dev -p ' + $frontendPort
Start-Process powershell -ArgumentList '-NoExit', '-Command', $frontendCmd -WindowStyle Normal

Write-Host 'Ambos os servidores foram iniciados em novas janelas do console!' -ForegroundColor Green
Write-Host ('  - Backend API: http://localhost:' + $backendPort) -ForegroundColor Gray
Write-Host ('  - Frontend Web: http://localhost:' + $frontendPort) -ForegroundColor Gray
Write-Host '==================================================' -ForegroundColor Cyan
