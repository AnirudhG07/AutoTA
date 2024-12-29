## Problem:

Let \(E\) and \(F\) be vector spaces (not assumed to be finite-dimensional). Let \(S:E\to F\) be a linear transformation.

1. Prove \(S(E)\) is a vector space.
2. Show \(S\) has a kernel \(\{0\}\) if and only if \(S\) is injective (i.e., one-to-one).
3. Assume \(S\) is injective; prove \(S^{-1}:S(E)\to E\) is linear.

## Solution:

1. For a linear transformation S between two vector spaces, we know that the image of the domain under S forms a vector space, and thus we have the result.

2. For a linear transformation S, we know that S is injective if and only if it takes 0 to 0. This proves that the kernel is a singleton set with only 0. On the other hand, if only 0 goes to 0, no other element can go to 0. We can extend this argument linearly to other elements of the vector space, and therefore, no two elements in the domain go to the same element in the codomain, making S injective.

3. For \(av+bw\in S(E)\) with \(v=S(x)\) and \(w=S(y)\), we have

\[S^{-1}(av+w) =S^{-1}(aS(x)+bS(y))\] \[=S^{-1}(S(ax+by))\] \[=ax+by\] \[=aS^{-1}(v)+bS^{-1}(w)\]

therefore, \(S^{-1}\) is linear.

