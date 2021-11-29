We appreciate the useful comments from reviewers to improve our paper. All typos pointed out in the comments are accepted and will be fixed in our final version. Below are our detailed responses to the reviews and misunderstandings.

## **To all reviewers**
* About the Significance of this paper

Compared to previous studies on solving BC, this paper first shows that the BCs computed from previous algorithms do not make much sense because they are usually trivial. We proposed a BC-solving method (SyntacBC) with the dominating performance advantage compared to the SOTA BC solver. With our efficient solving method and its reproducible results (compared to the uncertain results of learning methods), we saved more time and analyzed the solved BCs. Moreover, we observe that humans can not benefit from the computed BC. So we gave a thorough discussion on BC’s formal definition (Section 5). To ensure that BCs are valuable, more constraints need to be met.

Therefore, we provide a brand new method (SemanticBC) with the significant advantage on time consumption to solve the really helpful (or meaningful) BCs, which directly shows a sequence of events leading to the divergence of goals. This paper presents a new foundation of the BC solving method, hoping to improve the entire identify-assess-control flow of BCs and apply it to real industrial formal requirements or properties to find their incompleteness.

* About Table 2 and the Evaluation of SyntacBC

The way we compared the solver JFc to SyntacBC is described as follows: we run the solver JFc and SyntacBC on the same case, then SyntacBC can gain the result with a >1000X speed-up than JFc. This time consumption advantage can be obtained by comparing the column t_s of the two methods. Notably, both tools output a set of BCs. Let {BC_j} as the set solved by JFc and {BC_q} by SyntacBC, we use the filter metric introduced in the previous study to reduce the number of BCs in the set {BC_j, BC_q}. And the BCs in set {BC_q} are always considered by the filter metric to capture no divergence and should be reserved. The coverage in column ‘c’ represents what percentage of BCs in set {BC_j} will be computed to be redundant because of the BCs in set {BC_q}.

===
## **To reviewer A**
> Q1: Table 2 - please explain what is going on here as detailed in my comments above

A: Please refer to the answer to *About Table 2 and the evaluation of SyntacBC*.

> Q2: What is the (practical) significance of solving BCs in the examples listed in Table 2?

A: Table 2 shows the superiority of the SyntacBC method compared with the SOTA BC solving method. This makes us focus on the solved BCs, which leads to a discussion about understanding the meaning of BC. And the BCs solved by SemanticBC in Table 3 are of practical significance. They clearly show the finite sequence of events that lead to the divergence of the goals, and can be hardly solved by the previous method.

===
## **To reviewer B**
> Q1: What is the >1000X speed-up mentioned in the contributions?

A: This refers to the performance promotion of SyntacBC which shows in Table 2, and please refer to the answer to *About Table 2 and the evaluation of SyntacBC*.

>Q2: Where is the third contribution discussed?

A: It is composed of the discussion in Section 5 and the evaluation of SemanticBC. This is the first article that focuses on the meaning of the solved BCs. Our SyntacBC method shows that it is very easy to only consider the LTL Syntax to solve BCs. But we want to ensure that the solved BC really has the value for analysis, then other conditions need to be met. This discussion not only leads to our SemanticBC method, but also guides other researchers to think about this research question from the perspective of practical application.

> Q3: Why are not all the cases from Table 2 considered in Table 3?

A: That is because no BC is solved by SemanticBC in most omitted cases. And that means there is no BC-trace (a finite trace cause divergence) in these cases according to our proof (Theorem 6).

> Q4: What is the significance of this work?

A: Please refer to the answer to *About the Significance of this paper*.

> Q5: Where is the data to support the claims in Table 2 and 3?

A: In supplementary materials, Table 2 for SyntacBC in folder \case_result and Table 3 for SemanticBC in folder \case_result_aut.

> *L256* Q: Do we mix the meaning of domain properties and goals?

No. The mix-use allows the symbols *G* and *Dom* to serve as the meaning of LTL formulas and sets in different contexts, and this is only for the simplicity to explain our approach without introducing much more mathematical notations.

===
## **To reviewer C**
> Q1: Could you comment on the paragraph performance evaluation of my review?

A: Please refer to the answer to *About Table 2 and the evaluation of SyntacBC*.

> Q2: Could you comment on the paragraph evaluation of SemanticBC of my review?

A: We agree that the evaluation of SemanticBC looks more like a discussion than an evaluation, since the evaluation does not make a quantitative comparison. But we use the proof (in Section 6.1) and case study (in RQ1-3) to describe the effectiveness of SemanticBC. We wonder whether our misdescription of the research problem caused your misunderstanding, but we believe that RQ1 should be modified to ‘Does SemanticBC find meaningful BCs?’.

> *L328* Q:  Can divergence be solved intuitively by identifying precedences between goals?

A: The use of precedences here can only ensure that some goals are met, and what we want is that all goals are met under any circumstances, which is important in a safety critical system. In this MPC case, when the event h&m (high water level and methane in the environment) occurs, no matter which goal is to be met first, then a disaster will occur due to the unsatisfaction of the other goal (flooding or explosion).

> *L346-L347* Q: Are we selecting the BCs that are more general, and then identifying those that are more "helpful" to engineer?.

A: We are not proposing a method to choose the more helpful BCs from the results solved by JFc or SyntacBC. We define a form of BC (p_1&Xp_2&XXp_3&...) that can be intuitively understood, and then designed a method SemanticBC to directly solve it.

> *L689* Q: How we conclude 'the bc_q obtained by SyntacBC is always the witness of the bc_j obtained by JFc'?

A: This is also an experimental result, obtained by computing each element in the BCs set solved by the SyntacBC method with each by the JFc. If we put this data in Table 2, it may be a column of data with the same value '100%'.





