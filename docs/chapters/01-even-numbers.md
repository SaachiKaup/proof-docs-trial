# Even numbers

This short chapter demonstrates the reading interaction intended for longer proof documents.

<section class="reference-source" id="definition-even" data-reference-title="Definition 1.1: Even integers" markdown="1">

## Definition 1.1: Even integers

An integer $n$ is **even** when there is an integer $k$ such that $n = 2k$.

The integer $k$ is a witness to the claim that $n$ is even.

</section>

<section class="reference-source" id="lemma-even-square" data-reference-title="Lemma 1.2: Squaring preserves evenness" markdown="1">

## Lemma 1.2: Squaring preserves evenness

If $n$ is even, then $n^2$ is even.

**Proof.** By Definition 1.1, write $n = 2k$ for an integer $k$. Hence

$$
n^2 = (2k)^2 = 4k^2 = 2(2k^2).
$$

Since $2k^2$ is an integer, $n^2$ is even. $\square$

</section>

<section class="reference-source" id="theorem-even-sum" data-reference-title="Theorem 1.3: A sum of even squares is even" markdown="1">

## Theorem 1.3: A sum of even squares is even

Let $a$ and $b$ be even integers. Then $a^2 + b^2$ is even.

**Proof.** The hypothesis means that both $a$ and $b$ satisfy <button class="reference-trigger" type="button" data-reference="definition-even">Definition 1.1</button>. By <button class="reference-trigger" type="button" data-reference="lemma-even-square">Lemma 1.2</button>, both $a^2$ and $b^2$ are even. Thus there are integers $r,s$ for which $a^2 = 2r$ and $b^2 = 2s$. Therefore

$$
a^2 + b^2 = 2r + 2s = 2(r+s),
$$

and $r+s$ is an integer. So $a^2 + b^2$ is even. $\square$

The underlying algebra is the distributive law, stated in [OpenStax's elementary algebra text](https://openstax.org/books/elementary-algebra-2e/pages/1-6-the-commutative-and-associative-properties).

[^external-source]: OpenStax, *Elementary Algebra 2e*, ["The Commutative and Associative Properties"](https://openstax.org/books/elementary-algebra-2e/pages/1-6-the-commutative-and-associative-properties).

The proof uses only elementary integer algebra.[^external-source]

</section>
