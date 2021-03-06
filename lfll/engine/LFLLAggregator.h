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
#ifndef LFLLAGGREGATOR_H
#define LFLLAGGREGATOR_H

#include <cassert>

#include <lfll/engine/LFLLDefinitions.h>
#include <lfll/engine/LFLLMembership.h>
#include <lfll/engine/LFLLConsequence.h>
#include <lfll/norms/LFLLSNorm.h>

LFLL_BEGIN_NAMESPACE

/**
 * \brief Aggregate consequences to membership using a s-norm operator.
 *
 * It is useful if you want to chain up systems.
 * \tparam NT Number of terms
 * \tparam SNorm S-norm operator. Default is Max.
 */
template<size_t NT, typename SNorm = LFLLMax>
class LFLLAggregator
{
public:
    /**
     * \brief Constructor.
     * \param sNorm SNorm to be used. Value is passed by copy
     */
     
    LFLLAggregator(const SNorm sNorm = SNorm())
        : m_sNorm(sNorm)
    {}

	/**
	 * \brief Aggregate consequences to membership.
	 * \tparam NR Number of rules
	 * \param consequence Consequence to aggregate
	 * \return Membership result
	 */
	 
    template <size_t NR>
    LFLLMembership<NT> aggregateConsequence(
        const LFLLConsequence<NR>& consequence) const
    {
        LFLLMembership<NT> result;
        result.reset();
        for (size_t ruleIndex = 0 ; ruleIndex < NR ; ++ruleIndex) {
            const scalar consequenceValue =
                    consequence.getVal(ruleIndex);
            lfll_uint consequenceTermIndex =
                    consequence.getTermIndex(ruleIndex);
            if (consequenceTermIndex != 0) {
                --consequenceTermIndex;
                result.setVal(consequenceTermIndex, m_sNorm(
                    result.getVal(consequenceTermIndex), consequenceValue));
            } 

        }

        return result;
    }
    
private:
    const SNorm m_sNorm;
};

LFLL_END_NAMESPACE

#endif //LFLLAGGREGATOR_H
