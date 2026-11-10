import json
from pathlib import Path

projeto = Path(__file__).resolve().parent
caminho = projeto / "reports" / "relatorio-teste.json"

with caminho.open(encoding="utf-8") as arquivo:
    relatorio = json.load(arquivo)

for ip in relatorio["ips_em_alerta"]:
    falhas = relatorio["falhas_por_ip"][ip]
    print(f"Alerta: o IP {ip} apresentou {falhas} falhas.")
    