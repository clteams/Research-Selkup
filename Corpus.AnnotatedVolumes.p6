#!/usr/bin/perl6

grammar Annotated-Text1-Parser-Fabula {
  rule TOP {
    ^ [ <plain> || <section> ] $
  }
  token plain {
    <- [\(\)] - :digit> +
  }
  token number {
    <digit> +
  }
  token section {
    <number> ")" \s* <plain>
  }
}

grammar Annotated-Text1-Parser-Notation {
  rule TOP {
    ^ [ <break-plot> || <plain> || <section> ] $
  }
  token section {
    <:digit + [a .. z]> +
    "." \s* <plain>
  }
  token plain {
    [
      <- :digit> <- [\.]>
      ||
      <digit> + <- [a .. z]>
    ]
    .*
  }
  token break-plot {
    [
      "Пелек" ["а" || "а́"] "т" .*
      ||
      "-" \s* <digit>+ \s* "-"
    ]
  }
}
say Annotated-Text1-Parser-Fabula.parse('99) Придя, поел и лег, крепко');
