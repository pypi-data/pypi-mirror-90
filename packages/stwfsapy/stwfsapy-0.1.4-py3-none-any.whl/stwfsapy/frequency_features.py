# Copyright 2020 Leibniz Information Centre for Economics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License


from typing import Dict
from math import log
from collections import defaultdict
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError


class FrequencyTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.idfs_ = None

    def fit(self, X=None, y=None, **kwargs):
        doc_counts = defaultdict(int)
        doc_terms = set()
        n_docs = 0
        for x in X:
            doc_terms.add(x[0])
            if x[-1]:
                n_docs += 1
                for term in doc_terms:
                    doc_counts[term] += 1
        self.idfs_ = {
            concept: log(n_docs/doc_count)
            for concept, doc_count
            in doc_counts.items()
        }
        return self

    def transform(self, X) -> np.array:
        if self.idfs_ is None:
            raise NotFittedError()
        ret = np.zeros((len(X), 3))
        pointer_idx = 0
        doc_concept_counts: Dict[str, int] = defaultdict(int)
        doc_concepts = []
        for idx, x in enumerate(X):
            concept = x[0]
            doc_concepts.append(concept)
            doc_concept_counts[concept] += 1

            if x[-1]:
                num_concepts = sum(doc_concept_counts.values())
                term_freqs = {
                    concept: count/num_concepts
                    for concept, count
                    in doc_concept_counts.items()
                }
                for concept in doc_concepts:
                    ret[pointer_idx, 0] = term_freqs[concept]
                    concept_idf = self.idfs_.get(concept)
                    if concept_idf:
                        ret[pointer_idx, 1] = concept_idf
                        ret[pointer_idx, 2] = term_freqs[concept] / concept_idf
                doc_concept_counts = defaultdict(int)
                doc_concepts = []
        return ret
