"""A census: Yavuz Inal, User-Friendly Locations of Error Messages in Web Forms: An Eye Tracking Study, Journal of Eye Movement Research 9(5):1, 2016, whole.

A source is adopted entire or not at all (the source-the-rule protocol). The census unit is
each of the paper's own findings and the conclusions it draws from them, read on 2026-11-20 in
the full text (bop.unibe.ch/JEMR/article/view/2821, its PDF at
bop.unibe.ch/JEMR/article/download/2821/pdf-951; doi 10.16910/jemr.9.5.1): the four measures of
the Results, the participants' views, the Discussion and the threats to validity. The
literature review's rules are other authors' (Nielsen 2001, Brown 1983, Linderman and Fried
2004, Bargas-Avila et al. 2011, Seckler et al. 2012) and are not this paper's to census.

The paper states no rule craft-laws lacks. Its headline finding - an error message on the
right of its field is spotted fastest - is not statistically significant (the paper: "group
mean differences were not statistically significant for form completion time, error
recognition time, the number of saccades, and error correction time"), so it is set aside as a
finding, not routed as a rule. Its other conclusions are rules craft-laws already holds.
Seckler, Tuch, Opwis and Bargas-Avila 2012, whose title states "Put them on the right side of
the erroneous input field", is a separate source and was not opened.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20, which cited it for an error message beside its
field.

    python -m craft.census_inal
"""

from __future__ import annotations

_NS = "a finding the paper reports as not statistically significant; no rule"

# finding -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Form completion time: ... the ANOVA results yielded that differences between group means were not significant for form completion time": (
        "set aside", "", _NS),
    "The results of the study showed that the participants spotted the error message fastest when it was displayed on the right side of the erroneous input field.": (
        "set aside", "",
        _NS + " (p = 0.06); its direction agrees with error-lands-at-the-field"),
    "the total number of saccades was 244 for both the error messages displayed on the right of and below the erroneous input field. However, this number was significantly lower for the messages located at the top (217) and bottom (206) of the form.": (
        "set aside", "",
        "a finding about effort, which the abstract reports as not significant; no rule"),
    "The participants, who were presented the error messages on the right side of and below the erroneous input field, corrected the error in an average of 12.55 seconds and 12.68 seconds, respectively. However, when the error messages were displayed at the top and bottom of the form, the participants corrected them in shorter time": (
        "set aside", "", _NS),
    "This observation shows the importance of providing examples in error messages to instruct the users on how to correct the error.": (
        "covered", "error-says-the-fix", "the message instructs the fix"),
    "a significant number of the participants preferred a Web form design that places restrictions on data input related to the required format and contains tooltips or placeholders to inform the users about the correct format of the input.": (
        "set aside", "",
        "the participants' preference; a placeholder carrying the format is what "
        "no-placeholder-labels forbids, and the paper states no rule"),
    "they suggested that the system should give them feedback about the correct and incorrect input immediately after entering data in each field.": (
        "covered", "validate-at-field-exit", "checked as each field is left"),
    "almost all the participants who were offered the messages at the top or bottom of the form complained about the distance between the error message and the erroneous input field.": (
        "covered", "error-lands-at-the-field", "the message beside its field"),
    "Most participants stated that both required and erroneous input fields should be marked with a color to better capture their attention.": (
        "set aside", "",
        "the participants' preference; colour as one cue among others is allowed by "
        "colour-is-never-the-only-signal, and the paper states no rule"),
    "the generalization of the study findings may be problematic because the participants were all young adults and left-to-right readers and writers ... the participants had high levels of computer skills ... low statistical power ... single Web form": (
        "set aside", "", "the paper's threats to validity, which bound every finding above"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 10


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_inal",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the paper's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Inal 2016, error message locations: {len(CENSUS)} classified\n")
    for rule, (route, law, note) in CENSUS.items():
        print(f"  {route:<9} {rule}")
        if law:
            print(f"            -> {law}")
    print()
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    if missing:
        for rule, law in missing:
            print(f"\n  BROKEN  {rule} names law {law!r} and no such law exists")
        return 1
    print("\n  Every covered rule names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
