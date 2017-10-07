#!/usr/bin/perl6

grammar Annotated-Vol1-Text1-Parser-Fabula {
  rule TOP {
    ^ [
      <plain>
        ||
      <section>+ % [\s*]
      ] $
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

grammar Annotated-Vol1-Text1-Parser-Notation {
  rule TOP {
    ^ [ <void-string> || <section> || <plain> ] $
  }
  token section {
    <number>
    "." \s* <plain>
  }
  token number {
    <:digit + [a .. z]> +
  }
  token plain {
    [
      <- :digit> <- [\.]>
        ||
      <digit> + <- [a .. z]>
    ]
    .*
  }
  token void-string {
    [
      "Пелек" ["а" || "а́"] "т" .*
        ||
      "-" \s* <digit>+ \s* "-"
    ]
  }
}

grammar Annotated-Vol2-Text1-Parser-Fabula {
  rule TOP {
    ^ [
      <plain>
        ||
      <section>+ % [\s*]
      ] $
  }
  token plain {
    [
      <- [\(\)] - :digit> +
      ||
      \( <- [\)]>* \)
    ]
  }
  token number {
    <digit> +
  }
  token section {
    <number> ")" \s* <plain>
  }
}

grammar Annotated-Vol2-Text1-Parser-Notation {
  rule TOP {
    ^ [ <void-string> || <section> || <plain> ] $
  }
  token section {
    <number>
    "." \s* <plain>
  }
  token number {
    <:digit + [a .. z]> +
  }
  token plain {
    [
      <- :digit> <- [\.]>
        ||
      <digit> + <- [a .. z]>
    ]
    .*
  }
  token void-string {
    \s* <digit>+ \s*
  }
}

grammar Annotated-Vol3-Text1-Parser-Fabula {
  rule TOP {
    ^ [
      <void-string>
        ||
      <plain>
        ||
      <section>+ % [\s*]
      ] $
  }
  token void-string {
    \s* <digit>+ \s*
  }
  token plain {
    [
      <- [\(\)] - :digit> +
      ||
      \( <- [\)]>* \)
    ]
  }
  token number {
    <digit> +
  }
  token section {
    <number> ")" \s* <plain>
  }
}

grammar Annotated-Vol3-Text1-Parser-Notation {
  rule TOP {
    ^ [ <void-string> || <section> || <plain> ] $
  }
  token section {
    <number>
    "." \s* <plain>
  }
  token number {
    <:digit + [a .. z]> +
  }
  token plain {
    [
      <- :digit> <- [\.]>
        ||
      <digit> + <- [a .. z]>
    ]
    .*
  }
  token void-string {
    \s* <digit>+ \s*
  }
}

grammar Annotated-Vol4-Text1-Parser-Fabula {
  rule TOP {
    ^ [
      <void-string>
        ||
      <plain>
        ||
      <section>+ % [\s*]
      ] $
  }
  token void-string {
    \s* <digit>+ \s*
  }
  token plain {
    [
      <- [\(\)] - :digit> +
      ||
      \( <- [\)]>* \)
    ]
  }
  token number {
    <digit> +
  }
  token section {
    <number> ")" \s* <plain>
  }
}
