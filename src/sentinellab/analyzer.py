from collections import Counter
from pathlib import Path
import argparse
import json


def analyze(path, limit=5, as_json=False):
    total = 0
    failures = 0
    successes = 0
    failures_by_ip = Counter()
    with path.open(encoding="utf-8", errors="replace") as log:
        for line in log:
            if not line.strip():
                continue

            total += 1

            if "Failed password" in line:
                failures += 1

                parts = line.split() 

                if "from" in parts:
                    position = parts.index("from") + 1
                    if position < len(parts):
                        ip = parts[position]
                        failures_by_ip[ip] += 1 


            elif "Accepted password" in line:
                successes += 1
        if as_json:
            resultado = {
                "linhas_analisadas": total,
                "falhas": failures,
                "sucessos": successes,
                "limite": limit,
                "falhas_por_ip": dict(failures_by_ip),
                "ips_em_alerta": [
                ip for ip, count in failures_by_ip.items() if count >= limit
            ],
        }
            print(json.dumps(resultado, indent=2))
            return
    
    print("SentinelLab — Análise de autenticação SSH")
    print(f"Linhas analisadas: {total}")
    print(f"Falhas de autenticação: {failures}")
    print(f"Autenticações bem-sucedidas: {successes}")
    
    print("\nFalha por IP:")
    for ip, count in failures_by_ip.most_common():
        print(f" {ip}:{count}")
        if count >= limit: 
            print(f"  AVISO: limite de {limit} falhas atingido.")       

def main():
    parser = argparse.ArgumentParser(description="Analisa logs SSH.")
    parser.add_argument("log", type=Path, help="Arquivo de log")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="Exibe o relatório em JSON")
    args = parser.parse_args()
    if args.limit < 1: parser.error("--limit deve ser pelo menos 1")
    try:
        analyze(args.log, limit=args.limit, as_json=args.json)
    except OSError as error:
        parser.exit(1, f"Não foi possível ler o arquivo: {error}\n")


if __name__ == "__main__":
    main()
