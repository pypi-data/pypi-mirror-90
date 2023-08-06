.. raw:: html

    %path = "maths/differential/introduction"
    %kind = chindnum["texts"]
    %level = 12
    <!-- html -->

We will use the concepts:

- variable/value
- change
- velocity

Variable/Value
==============

English is a historical mix of two languages.
So there are two words of many things.
*Change*, for example, can also be called *vary*.
That's why something, that can change, is called a *variable*.

A variable assumes one *value* at a time, *exclusively*.
It does not need to be "at a time".
It could also be "at a place".

As a side-note:
The uniqueness is expressed by the word *function*:
We can say, the value is a *function* of this or that.

We can use a number to denote a *value*.
We could also use a word, but it is easier with a number.

Variable = {value1, value2, ...}
Position = {10m , 20m, ..., 120m, ...}

Change
======

We assume a gradual change.

Large changes:

    The change is expressed with a difference: `-`.
    Difference is abbreviated with a Greek D: Δ.

    `Δy_1 = y_1 - y_0`.

    The differences can be added to get the full extend of the variable.
    We basically undo the difference (subtraction) by addition.

    `y = Σ Δy_i = Δy_1 + Δy_2 + ...`.


Small changes:

    We use ``d`` instead of ``Δ`` for very small changes.

    `dy = (y + dy) - y`.

    `d` is called *differential*.

    With `dy` we use `∫` for sum,
    and call it *integral*.

Velocity
========

How fast a value changes is again a variable.
It is called *speed* or *velocity* of change of that variable.

Velocity is relative.
To describe velocity of change of the value of one variable
we need *another variable* to compare it to.
Often this other variable is *time*, but it could be something else.
If there is no other variable specified, then it is implicitly *time*,
or better our time feeling, given by how fast our brain thinks.

Lets find the velocity by which you grow.
We have two variables:

1) Height `y`: The distance from the floor to the top of your head.
2) Age `x`: The number of years that have passed since your birth.

Differences:

    The *average* velocity over `Δx` is found by *dividing* the differences:

    `\tilde{v} = Δy/Δx`

    Why *divide*?
    *Because* then you can *multiply* to get back the difference:

    `Δy = \tilde{v} Δx`

    And you can sum the differences to get back the height:

    `y = Σ Δy = Σ \tilde{v} Δx`

Differentials:

    This velocity is at a specific `x` because `dx` is so small that we can neglect it.

    `v = dy/dx`

    and to get back y we sum the very many `v dx`

    `y = ∫ dy = ∫ v dx`.

    Velocity is used if `x` is time.
    More generally, one calls it *derivative*:

    - *derivative* of height `y` with respect to age `x`

Summary
=======

Change is expressed via differences,

- that `Δ` means *difference*
- that `d` means very small difference or *differential*

The symbol for sum is

- `Σ`, if summing differences
- `∫`, if summing differentials

Velocity is a quotient between two differences

- average over `Δx`: `\tilde{v}=\frac{Δy}{Δx}`
- at `x`: `v=\frac{dy}{dx}`

