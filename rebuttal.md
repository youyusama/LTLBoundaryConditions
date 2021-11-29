thank… We will first address the shared comments and then respond to questions/comments specific to each review. 

# **Response to all reviewers**

*Significance*
There have been some previous studies on solving BC, but our research first shows that although BCs solved by algorithms without considering its semantics satisfies the definition, it does not make much sense to get them because they are usually trivial. We proposed a BC solving method (SyntaxBC) with dominating performance advantage compared to the SOTA BC solver. With our efficient solving method and its repeatable characteristics (compared to the uncertain results of learning methods), we saved more time and analyzed the experiment results of the solved BCs. And we found that humans can not benefit from them. So we gave a deep discussion on BC’s formal definition (Section 5). To ensure that BCs have the value to be analyzed, more constraints need to be met. Furthermore, we provide a brand new method (SemanticBC) also with the excellent advantage on time consumption to solve the really helpful (or meaningful) BCs, which directly shows a sequence of events leading to the divergence of goals. This article is a new foundation of the BC solving method, for our hope to soonly improve the entire identify-assess-control flow of BCs and apply it to real industrial formal requirements or properties to find their incompleteness.

*Table 2 and the evaluation of SyntaxBC*
The way we compared the solver JFc and SyntaxBC could be understood like this: we run the solver JFc and SyntaxBC on the same case, then SyntaxBC has >1000X speed of JFc to give out a result, which is a set of BCs. Let {BC_j} as the set solved by JFc and {BC_q} by SyntaxBC, we use the filter metric introduced in the previous study to reduce the number of BCs in the set {BC_j, BC_q}. And the BCs in set {BC_q} are always considered by the filter metric to capture no less divergence and should be reserved. The coverage in column ‘c’ represents what percentage of BCs in set {BC_j} will be computed to be redundant because of the BCs in set {BC_q}. 
t_e

*Presentation?*
cutting something and more examples? crosscutting?


===
# **Response to reviewer A**
> Q1: Table 2 - please explain what is going on here as detailed in my comments above

Please refer to the answer to *Table 2 and the evaluation of SyntaxBC*.

> Q2: What is the (practical) significance of solving BCs in the examples listed in Table 2?

Table 2 shows the superiority of the SyntaxBC method compared with the SOTA BC solving method. It is not only an advantage in time consumption, but also the results are considered more valuable by the filter metric. This makes us focus on the solved bc, which leads to a discussion about understanding the meaning of bc.

===
# **Response to reviewer B**
> Q1: What is the >1000X speed-up mentioned in the contributions?

This refers to the performance promotion of SyntaxBC which shows in Table 2, and please refer to the answer to *Table 2 and the evaluation of SyntaxBC*.

> Q2: Where is the third contribution discussed?

It is composed of the discussion in Section 5 and the evaluation of SemanticBC.

> Q3: Why are not all the cases from Table 2 considered in Table 3?

Because no BC is solved in most omitted cases. And that means there is no BC-trace in these cases according to our proof(Theorem 6).

> Q4: What is the significance of this work?

Please refer to the answer to *Significance*.

> Q5: Where is the data to support the claims in Table 2 and 3?

In supplementary materials, Table 2 for SyntaxBC in folder \case_result and Table 3 for SyntaxBC in folder \case_result_aut.


===
# **Response to reviewer C**
> Q1: Could you comment on the paragraph performance evaluation of my review?

Please refer to the answer to *Table 2 and the evaluation of SyntaxBC*.

> Q2: Could you comment on the paragraph evaluation of SemanticBC of my review?

The evaluation of SemanticBC does seem to be more like a discussion than an evaluation. However, this is because it is difficult to quantify indicators such as 'meaningful' or 'easy to be understood' to obtain a numerical comparison table. But it is possible to analyze the results through specific examples. Maybe we have a deviation in the definition of ‘easier to understand’. The BC we obtained by SemanticBC has the form of p_1&Xp_2&XXp_3&...(& for and, X for next). As an BC, it represents a clear event trace that can trigger a divergence. Such as a&b&X(a&!b) stands for the occurrence of events a and b at the current moment and the occurrence of events a and !b at the next moment.

===
# **Detailed revision**
We give responses and revisions according to the line numbers.

*L66*

*L75*

*L82-L88* 

*L97* We supplement the corresponding reference.

*L98-L101* We will describe it as an observation of author 7 in the amendment.

*L102* ?

*L108* We will add a reference of [27] here.

*123*

*128*

*L149-L157*

*L180-L217* We will modify the inconsistency of symbols.

*L256* The mix-use allows the symbols *G* and *Dom* to serve as the meaning of LTL formulas and sets in different contexts, otherwise we would need to define a large number of additional symbols, which will make the article more difficult to understand.

*L260* Here we refer to the methodology mentioned in article [27], and we will add this reference in the revision.

*L328* The use of precedences here can only ensure that some goals are met, and what we want is that all goals are met under any circumstances. When the event h&m (high water level and methane in the environment) occurs, no matter which goal is to be met first, then a disaster will occur due to the unsatisfaction of the other goal (flooding or explosion).

*L346-L347* We are not proposing a method to choose a more helpful BC from the results solving by JFc or SyntaxBC. We define a form of BC (p_1&Xp_2&XXp_3&...) that can be intuitively understood, and then designed a method SemanticBC to directly solve it.

*L349 Fig 1* We will add content in the caption and illustration to make the description of the picture clearer.

*L383* We will modify 'g_i' to 'g_1 or g_2'

*L554* We will modify it to capital as 'Property'.

*L582*

*L664*

*L664-L667*

*L689* This is also an experimental result, obtained by computing each element in the BCs set solved by the SyntaxBC method with each by the JFc.

*L659-L660* Both of our methods refer to this experimental setups, and we will add this description in revision.

*L699-L707* We do find that we have less content to illustrate why BC solved by previous method and the SyntaxBC are difficult to understand. We just used a simple example and MPC example to answer this question in the Q2 of Section 5.

*L714* We will modify 'lemma 2' to 'Theorem 2'.

*L714* We will revise this grammatical error.

*L753* We supplement the corresponding reference.

*L938*
