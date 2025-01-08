## Problem:

For \(n\) a positive integer, let \(d(n)\) denote the number of positive integers that divide \(n\). Prove that \(d(n)\) is odd if and only if n is a perfect square.

## Solution:

Let

\[n=p*{1}^{k*{1}}p*{2}^{k*{2}}\cdots p*{n}^{k*{n}}\]

be the factorization into a product of prime powers (\(p*{1}<p*{2}<\cdots<p\_{n}\)) for \(n\). The positive integer divisors of \(n\) are then the numbers

\[p*{1}^{j*{1}}p*{2}^{j*{2}}\cdots p*{n}^{j*{n}}\qquad 0\leq j\leq k\_{j}.\]

It follows that \(d(n)\) is the number of \(r\)-tuples \((j*{1},j*{2},\ldots,j\_{r})\) satisfying the preceding conditions. In other words,

\[d(n)=(k*{1}+1)(k*{2}+1)\cdots(k\_{n}+1),\]

which is odd iff each \(k\_{i}\) is even; in other words, iff \(n\) is a perfect square.
