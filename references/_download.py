# Historical script, 18 May 2026. "Ghost in the Machine" was the project's
# working title at that date. Run from the repository root:
#     python references/_download.py
"""Download 15 recent arXiv PDFs (2021-2026) for the Ghost in the Machine project.

Each entry: (arxiv_id, output_filename, short_topic).
arXiv IDs verified via WebSearch on 2026-05-18.
"""
import os
import sys
import time
import urllib.request

DEST = os.path.dirname(os.path.abspath(__file__))

# Format: (arxiv_id, output_filename, topic_tag)
PAPERS = [
    # --- Tier 1: directly addresses project's core questions ---
    ("2210.01282", "01_Zeng2024_StructEstMDP_HighDim.pdf",
     "ML-IRL bridge between DDC and MaxEnt IRL (Operations Research 2024)"),
    ("2411.15951", "02_Skalse2024_PartialIdentifiability_IRL.pdf",
     "Partial identifiability + misspecification in IRL"),
    ("2412.11155", "03_Skalse2024_NonExponentialDiscounting_IRL.pdf",
     "Partial identifiability with non-exponential discounting"),
    ("2306.00629", "04_Kim2023_Identifiability_ConstrainedIRL.pdf",
     "Identifiability + generalizability in constrained IRL"),
    ("2106.03498", "05_Cao2021_Identifiability_IRL.pdf",
     "Foundational identifiability in inverse reinforcement learning"),
    ("2405.12467", "06_Bruneel2024_CCP_FiniteDependence.pdf",
     "CCP estimator with 2-period finite dependence (extends Arcidiacono-Miller)"),
    ("2403.16829", "07_Cao2024_EntropyReg_IRL_Convergence.pdf",
     "Convergence of model-free entropy-regularized IRL algorithm"),

    # --- Tier 2: supporting context ---
    ("2409.07569", "08_Liu2024_ConstrainedIRL_Survey.pdf",
     "Survey of inverse constrained reinforcement learning"),
    ("2503.17865", "09_Skalse2025_Understanding_IRL.pdf",
     "Understanding inverse reinforcement learning"),
    ("2510.03013", "10_Liu2025_Distributional_IRL.pdf",
     "Distributional inverse reinforcement learning"),

    # --- Tier 3: additional context ---
    ("2510.08526", "11_Bellemare2025_EntropyReg_DistRL_Convergence.pdf",
     "Convergence theorems for entropy-regularized + distributional RL"),
    ("2202.04339", "12_NoretsShimizu2022_SemiparBayes_DDC.pdf",
     "Semiparametric Bayesian estimation of DDC models"),
    ("2501.01669", "13_Zhi2025_TransferableRewards_AbstractedStates.pdf",
     "Inversely learning transferable rewards via abstracted states"),
    ("2511.02701", "14_Hu2025_ContinuousTime_DDCGames.pdf",
     "Identification + estimation of continuous-time DDC games"),
    ("2504.13241", "15_Ghanem2025_Recursive_DeepIRL.pdf",
     "Recursive deep inverse reinforcement learning"),
]


def download_pdf(arxiv_id: str, out_path: str) -> tuple[bool, str]:
    """Download one arXiv PDF. Returns (success, msg)."""
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
        # Verify it's actually a PDF
        if not data.startswith(b"%PDF"):
            return False, f"not a PDF (first bytes: {data[:20]!r})"
        with open(out_path, "wb") as f:
            f.write(data)
        return True, f"{len(data) // 1024} KB"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main():
    print(f"Destination: {DEST}\n")
    print(f"{'#':>3}  {'arXiv ID':<12}  {'Status':<10}  Filename")
    print("-" * 100)
    successes = []
    failures = []
    for i, (arxiv_id, filename, topic) in enumerate(PAPERS, 1):
        out_path = os.path.join(DEST, filename)
        ok, msg = download_pdf(arxiv_id, out_path)
        status = "OK" if ok else "FAIL"
        print(f"{i:>3}. {arxiv_id:<12}  {status:<10}  {filename}  [{msg}]")
        if ok:
            successes.append((arxiv_id, filename, topic))
        else:
            failures.append((arxiv_id, filename, topic, msg))
        time.sleep(3)  # be polite to arXiv

    print()
    print(f"Downloaded: {len(successes)}/{len(PAPERS)}")
    if failures:
        print("\nFailures:")
        for arxiv_id, filename, topic, msg in failures:
            print(f"  {arxiv_id}: {msg}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
