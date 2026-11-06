from collections import Counter
from pathlib import Path
import argparse



def analyze(path, limit=5):
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
    args = parser.parse_args()
    if args.limit < 1: parser.error("--limit deve ser pelo menos 1")
    try:
        analyze(args.log, limit=args.limit)
    except OSError as error:
        parser.exit(1, f"Não foi possível ler o arquivo: {error}\n")


if __name__ == "__main__":
    main()
