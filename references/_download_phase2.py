"""Phase 2: download 4 additional finance/applied-IRL references (refs 16-19).

These close the 'finance IRL applications' gap identified in INDEX.md phase 1.
All 4 are arXiv-available (Zelman et al. ICAIF '24 is ACM-paywalled and noted separately).
"""
import os
import sys
import time
import urllib.request

DEST = os.path.dirname(os.path.abspath(__file__))

PAPERS = [
    ("2507.04396", "16_Krishnamurthy2025_IRL_RevealedPreferences.pdf",
     "IRL using revealed preferences + passive stochastic optimization — bridges microeconomics and IRL"),
    ("2509.21172", "17_vanderLaan2025_IRL_ClassificationRegressions.pdf",
     "van der Laan/Kallus/Bibaut — IRL via classification + regressions; cross-listed in econ.EM"),
    ("2511.18076", "18_GIRL2025_PortfolioOptimization.pdf",
     "Portfolio optimization via GIRL (Gradient Inverse RL); finance IRL application"),
    ("2410.07525", "19_OfflineICRL2024_Healthcare.pdf",
     "Offline ICRL for safety-critical decisions in healthcare — IRL precedent in high-stakes applied domain"),
]


def download_pdf(arxiv_id: str, out_path: str) -> tuple[bool, str]:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "GhostInTheMachine-References/1.0 "
                "(academic; adityamaiti.123@gmail.com)"
            )
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        if not data.startswith(b"%PDF"):
            return False, f"not a PDF (first bytes: {data[:20]!r})"
        with open(out_path, "wb") as f:
            f.write(data)
        return True, f"{len(data) // 1024} KB"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main():
    print(f"Destination: {DEST}\n")
    successes, failures = [], []
    for i, (arxiv_id, filename, topic) in enumerate(PAPERS, 16):
        out_path = os.path.join(DEST, filename)
        ok, msg = download_pdf(arxiv_id, out_path)
        status = "OK" if ok else "FAIL"
        print(f"{i:>3}. {arxiv_id:<12}  {status:<10}  {filename}  [{msg}]")
        if ok:
            successes.append((arxiv_id, filename, topic))
        else:
            failures.append((arxiv_id, filename, topic, msg))
        time.sleep(3)
    print(f"\nDownloaded: {len(successes)}/{len(PAPERS)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
