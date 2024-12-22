## Problem:

Let \(E\) and \(F\) be vector spaces (not assumed to be finite-dimensional). Let \(S:E\to F\) be a linear transformation.

1. Prove\_ \(S(E)\) \_is a vector space.
2. Show* \(S\) \_has a kernel* \(\{0\}\) _if and only if_ \(S\) \_is injective (i.e., one-to-one).
3. Assume* \(S\) \_is injective; prove* \(S^{-1}:S(E)\to E\) \_is linear.

## Solution:

1.  We need to show that vector addition and scalar multiplication are closed in \(S(E)\), but this is a trivial verification because if \(v=S(x)\) and \(w=S(y)\) are vectors in \(S(E)\), then

\[v+w=S(x+y)\ \ \ \text{and}\ \ \ cv=S(cx)\]

are also in \(S(E)\).

2. If \(S\) is not injective, then two different vectors \(x\) and \(y\) have the same image \(S(x)=S(y)=v\), so

\[S(x-y)=S(x)-S(y)=v-v=0\]

that is, \(x-y\neq 0\) is a vector in the kernel of \(S\). On the other hand, if \(S\) is injective, it only takes \(0\in E\) into \(0\in F\), showing the result.

3. Assuming that \(S\) is injective, the application \(S^{-1}:S(E)\to E\) is well defined. Given \(av+bw\in S(E)\) with \(v=S(x)\) and \(w=S(y)\), we have

\[S^{-1}(av+w) =S^{-1}(aS(x)+bS(y))\] \[=S^{-1}(S(ax+by))\] \[=ax+by\] \[=aS^{-1}(v)+bS^{-1}(w)\]

therefore, \(S^{-1}\) is linear.
