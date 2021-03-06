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

#include "LFLLSimpleMamdani.h"

namespace
{

	const size_t NbInputs = 2;
	const size_t NbOutputs = 1;
	const size_t NbRules = 12;

	const size_t NbMfsForInput1 = 4;
	const size_t NbMfsForInput2 = 3;

	const LFLLGaussian i1mf1(0.200, 0.200);
	const LFLLTrapezoid i1mf2(0.000, 0.350, 0.550, 1.000);
	const LFLLPiShape i1mf3(0.000, 0.730, 0.790, 1.000);
	const LFLLSShape i1mf4(0.000, 1.000);

	const LFLLTriangle i2mf1(-0.060, 0.500, 1.000);
	const LFLLRectangle i2mf2(0.110, 0.370);
	const LFLLSigmoid i2mf3(5.000, 0.400);

	const LFLLBell o1mf1(0.250, 3.000, 0.260);
	const LFLLSigmoid o1mf2(20.000, 0.500);

	const LFLLRules<NbInputs, NbRules, NbOutputs> rules = {{
		{{1, 1}, {1}, 1, false},
		{{1, 2}, {2}, 1, false},
		{{1, 3}, {1}, 1, false},
		{{2, 1}, {2}, 1, false},
		{{2, 2}, {1}, 1, false},
		{{2, 3}, {2}, 1, false},
		{{3, 1}, {1}, 1, false},
		{{3, 2}, {2}, 1, false},
		{{3, 3}, {1}, 1, false},
		{{4, 1}, {2}, 1, false},
		{{4, 2}, {1}, 1, false},
		{{4, 3}, {2}, 1, false}
	}};
	const LFLLRulesEngine<NbInputs, NbRules, NbOutputs> rulesEngine(rules);


	typedef LFLLTuple<
		const LFLLGaussian,
		const LFLLTrapezoid,
		const LFLLPiShape,
		const LFLLSShape
	> Input1Tuple;
	const Input1Tuple input1Tuple = makeLFLLTuple(
		i1mf1, i1mf2, i1mf3, i1mf4);
	const LFLLInputFuzzifier<Input1Tuple> input1Fuzzifier(input1Tuple);

	typedef LFLLTuple<
		const LFLLTriangle,
		const LFLLRectangle,
		const LFLLSigmoid
	> Input2Tuple;
	const Input2Tuple input2Tuple = makeLFLLTuple(
		i2mf1, i2mf2, i2mf3);
	const LFLLInputFuzzifier<Input2Tuple> input2Fuzzifier(input2Tuple);


	typedef LFLLTuple<
		const LFLLBell,
		const LFLLSigmoid
	> Output1Tuple;
	const Output1Tuple output1Tuple = makeLFLLTuple(
		o1mf1, o1mf2);
	const LFLLMamdaniDefuzzifier<Output1Tuple,
		LFLLMamdaniBisector, LFLLMin, LFLLMax>
		output1Defuzzifier(output1Tuple, 0.000, 1.000);

}


void SimpleMamdani::process(
		const LFLLArray<2>& inputs,
		LFLLArray<1>& outputs)
{
	const LFLLMembership<NbMfsForInput1> antecedent1 =
		input1Fuzzifier.fuzzifyVariable(inputs[0]);
	const LFLLMembership<NbMfsForInput2> antecedent2 =
		input2Fuzzifier.fuzzifyVariable(inputs[1]);

	LFLLConsequence<NbRules> consequence1;

	typedef LFLLTuple<
		const LFLLMembership<NbMfsForInput1>,
		const LFLLMembership<NbMfsForInput2>
	> AntecedentTuple;

	typedef LFLLTuple<
		LFLLConsequence<NbRules>
	> ConsequenceTuple;

	const AntecedentTuple antecedents = makeLFLLTuple(
		antecedent1, antecedent2);

	ConsequenceTuple consequences = makeLFLLTuple(
		consequence1);

	rulesEngine.applyRules(antecedents, consequences);

	outputs[0] = output1Defuzzifier.defuzzifyConsequence(consequence1);
}
