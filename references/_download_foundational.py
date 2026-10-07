"""Download foundational (pre-2021) PDFs invoked by MATHEMATICAL_MODELLING_V11.md.

These complete the references/ folder so that EVERY citation in V11 corresponds
to a downloadable PDF on disk. URLs are author-page or open-access copies
verified via web search on 18 May 2026.
"""
import os
import sys
import time
import urllib.request

DEST = os.path.dirname(os.path.abspath(__file__))

# Format: (filename, url, citation)
PAPERS = [
    ("F01_Rust1987_OptimalReplacement_BusEngines.pdf",
     "http://www.its.caltech.edu/~mshum/stats/rust.pdf",
     "Rust (1987) Econometrica 55(5) — bus engine DDC foundation"),

    ("F02_HotzMiller1993_CCP_DynamicModels.pdf",
     "http://www.its.caltech.edu/~mshum/gradio/papers/condChoiceProbEstDynModel1993.pdf",
     "Hotz & Miller (1993) RES 60(3) — CCP inversion"),

    ("F03_Ziebart2008_MaxEntIRL_AAAI.pdf",
     "https://cdn.aaai.org/AAAI/2008/AAAI08-227.pdf",
     "Ziebart, Maas, Bagnell, Dey (2008) AAAI — MaxEnt IRL"),

    ("F04_MagnacThesmar2002_IdentifyingDDC.pdf",
     "https://www.its.caltech.edu/~mshum/gradio/papers/IDDDP.pdf",
     "Magnac & Thesmar (2002) Econometrica 70(2) — DDC identification"),

    ("F05_Pulvino1998_AssetFireSales_Aircraft.pdf",
     "https://web.stanford.edu/~piazzesi/Reading/Pulvino%201998.pdf",
     "Pulvino (1998) J. Finance 53(3) — fire-sale discounts on aircraft"),

    ("F06_RameyShapiro2001_DisplacedCapital_Aerospace.pdf",
     "https://public.websites.umich.edu/~shapiro/papers/jpe2001-jpe.pdf",
     "Ramey & Shapiro (2001) JPE 109(5) — displaced capital aerospace"),

    ("F07_Rust1997_RandomizationCurseDimensionality.pdf",
     "https://editorialexpress.com/jrust/crest_lectures/randomization.pdf",
     "Rust (1997) Econometrica 65(3) — random-grid discretization"),

    ("F08_McFadden1974_ConditionalLogit.pdf",
     "https://eml.berkeley.edu/reprints/mcfadden/zarembka.pdf",
     "McFadden (1974) Frontiers in Econometrics — conditional logit"),

    ("F09_ArcidiaconoEllickson2011_PracticalMethods_DDC.pdf",
     "https://public.econ.duke.edu/~psarcidi/annualreview5revision.pdf",
     "Arcidiacono & Ellickson (2011) Annual Review Econ. 3 — DDC survey"),

    ("F10_Haarnoja2017_SoftQLearning_DeepEnergyPolicies.pdf",
     "https://arxiv.org/pdf/1702.08165",
     "Haarnoja, Tang, Abbeel, Levine (2017) ICML — soft Q-learning / energy-based policies"),
]


def download_pdf(url: str, out_path: str) -> tuple[bool, str]:
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
        with urllib.request.urlopen(req, timeout=90) as resp:
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
    print(f"{'#':>3}  {'Filename':<70}  Status")
    print("-" * 110)
    successes, failures = [], []
    for i, (filename, url, cite) in enumerate(PAPERS, 1):
        out_path = os.path.join(DEST, filename)
        ok, msg = download_pdf(url, out_path)
        status = "OK" if ok else "FAIL"
        print(f"{i:>3}. {filename:<70}  {status} [{msg}]")
        if ok:
            successes.append((filename, url, cite))
        else:
            failures.append((filename, url, cite, msg))
        time.sleep(3)
    print()
    print(f"Downloaded: {len(successes)}/{len(PAPERS)}")
    if failures:
        print("\nFailures (paywalled or 404):")
        for filename, url, cite, msg in failures:
            print(f"  {filename}")
            print(f"    URL: {url}")
            print(f"    Reason: {msg}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
