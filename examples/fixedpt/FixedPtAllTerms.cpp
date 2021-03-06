/*
The MIT License (MIT)

Copyright (c) 2013 Nicolas Pauss

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#include "FixedPtAllTerms.h"

namespace
{

	const size_t NbInputs = 1;
	const size_t NbOutputs = 1;
	const size_t NbRules = 16;

	const size_t NbMfsForInput1 = 16;

	const LFLLBell i1mf1(0.4f, 3.0f, 0.0f);
	const LFLLBoolean i1mf2(1.f);
	const LFLLGaussian i1mf3(0.3f, 0.0f);
	const LFLLGaussianProduct i1mf4(0.239f, -0.197f, 0.28f, 0.0645f);
	const LFLLLRamp i1mf5(-1.0f, 1.0f);
	const LFLLPiShape i1mf6(-1.0f, -0.05f, 0.1f, 1.0f);
	const LFLLRectangle i1mf7(-0.75f, 0.4f);
	const LFLLRRamp i1mf8(-1.0f, 1.0f);
	const LFLLSigmoid i1mf9(5.0f, 0.0f);
	const LFLLSigmoidDifference i1mf10(8.77f, -0.442f, 12.5f, 0.468f);
	const LFLLSigmoidProduct i1mf11(8.14f, -0.336f, -8.82f, 0.421f);
	const LFLLSingleton i1mf12(0.2f);
	const LFLLSShape i1mf13(-1.0f, 1.0f);
	const LFLLTrapezoid i1mf14(-1.0f, 0.01f, 0.15f, 1.0f);
	const LFLLTriangle i1mf15(-1.0f, 0.01f, 1.0f);
	const LFLLZShape i1mf16(-1.0f, 1.0f);

	const LFLLSugenoZeroOrderTerm o1t1 = {0.4f};
	const LFLLSugenoFirstOrderTerm<1> o1t2 = {0.2f, -0.8f};
	const LFLLSugenoZeroOrderTerm o1t3 = {0.3f};
	const LFLLSugenoFirstOrderTerm<1> o1t4 = {0.239f, 0.0645f};
	const LFLLSugenoZeroOrderTerm o1t5 = {-1.0f};
	const LFLLSugenoFirstOrderTerm<1> o1t6 = {-1.0f, -0.05f};
	const LFLLSugenoZeroOrderTerm o1t7 = {-0.75f};
	const LFLLSugenoFirstOrderTerm<1> o1t8 = {-1.0f, 1.0f};
	const LFLLSugenoZeroOrderTerm o1t9 = {0.15f};
	const LFLLSugenoFirstOrderTerm<1> o1t10 = {0.77f, -0.442f};
	const LFLLSugenoZeroOrderTerm o1t11 = {0.14f};
	const LFLLSugenoFirstOrderTerm<1> o1t12 = {0.2f, -0.8f};
	const LFLLSugenoZeroOrderTerm o1t13 = {1.0f};
	const LFLLSugenoFirstOrderTerm<1> o1t14 = {-1.0f, 0.01f};
	const LFLLSugenoZeroOrderTerm o1t15 = {-0.25f};
	const LFLLSugenoFirstOrderTerm<1> o1t16 = {-1.0f, 1.0f};

	const LFLLRules<NbInputs, NbRules, NbOutputs> rules = {{
		{{1}, {16}, 1.f, false},
		{{2}, {15}, 0.9f, false},
		{{3}, {14}, 0.8f, false},
		{{4}, {13}, 0.7f, false},
		{{5}, {12}, 0.6f, false},
		{{6}, {11}, 0.5f, false},
		{{7}, {10}, 0.4f, false},
		{{8}, {9}, 0.3f, false},
		{{9}, {8}, 0.3f, false},
		{{10}, {7}, 0.4f, false},
		{{11}, {6}, 0.5f, false},
		{{12}, {5}, 0.6f, false},
		{{13}, {4}, 0.7f, false},
		{{14}, {3}, 0.8f, false},
		{{15}, {2}, 0.9f, false},
		{{16}, {1}, 1.f, false}
	}};
	const LFLLRulesEngine<NbInputs, NbRules, NbOutputs> rulesEngine(rules);


	typedef LFLLTuple<
		const LFLLBell,
		const LFLLBoolean,
		const LFLLGaussian,
		const LFLLGaussianProduct,
		const LFLLLRamp,
		const LFLLPiShape,
		const LFLLRectangle,
		const LFLLRRamp,
		const LFLLSigmoid,
		const LFLLSigmoidDifference,
		const LFLLSigmoidProduct,
		const LFLLSingleton,
		const LFLLSShape,
		const LFLLTrapezoid,
		const LFLLTriangle,
		const LFLLZShape
	> Input1Tuple;
	const Input1Tuple input1Tuple = makeLFLLTuple(
		i1mf1, i1mf2, i1mf3, i1mf4, i1mf5, i1mf6, i1mf7, i1mf8, 
		i1mf9, i1mf10, i1mf11, i1mf12, i1mf13, i1mf14, i1mf15, i1mf16);
	const LFLLInputFuzzifier<Input1Tuple> input1Fuzzifier(input1Tuple);


	typedef LFLLTuple<
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>,
		const LFLLSugenoZeroOrderTerm,
		const LFLLSugenoFirstOrderTerm<1>
	> Output1Tuple;
	const Output1Tuple output1Tuple = makeLFLLTuple(
		o1t1, o1t2, o1t3, o1t4, o1t5, o1t6, o1t7, o1t8, 
		o1t9, o1t10, o1t11, o1t12, o1t13, o1t14, o1t15, o1t16);
	const LFLLSugenoDefuzzifier<Output1Tuple, LFLLSugenoWeightedAverage>
		output1Defuzzifier(output1Tuple);

}


void FixedPtAllTerms::process(
		const LFLLArray<1>& inputs,
		LFLLArray<1>& outputs)
{
	const LFLLMembership<NbMfsForInput1> antecedent1 =
		input1Fuzzifier.fuzzifyVariable(inputs[0]);

	LFLLConsequence<NbRules> consequence1;

	typedef LFLLTuple<
		const LFLLMembership<NbMfsForInput1>
	> AntecedentTuple;

	typedef LFLLTuple<
		LFLLConsequence<NbRules>
	> ConsequenceTuple;

	const AntecedentTuple antecedents = makeLFLLTuple(
		antecedent1);

	ConsequenceTuple consequences = makeLFLLTuple(
		consequence1);

	rulesEngine.applyRules(antecedents, consequences);

	outputs[0] = output1Defuzzifier.defuzzifyConsequence(inputs, consequence1);
}
