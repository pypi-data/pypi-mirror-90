// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    applyFiltersToColumn,
    checkColumn,
    checkSheet,
    tryTest
} from '../utils/helpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

fixture `Test Filter`
    .page(CURRENT_URL)

// See here: https://devexpress.github.io/testcafe/documentation/recipes/basics/test-select-elements.html
test('Test single filter conditions, string column', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            const filterTests = [
                {
                    filterCondition: 'contains',
                    filterValue: '1',
                    columnValues: ['123', '1']
                },
                {
                    filterCondition: 'does not contain',
                    filterValue: '1',
                    columnValues: ['2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: 'is exactly',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'A', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'A', filterTests[i].columnValues)
            }
        }
    )
});

// See here: https://devexpress.github.io/testcafe/documentation/recipes/basics/test-select-elements.html
test('Test single filter conditions, mixed column', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            const filterTests = [
                {
                    filterCondition: 'contains',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'does not contain',
                    filterValue: '1',
                    columnValues: ['123', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: 'is exactly',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'C', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'C', filterTests[i].columnValues)
            }
        }
    )
});


test('Test single filter conditions, number column', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            
            // See: https://devexpress.github.io/testcafe/documentation/guides/basic-guides/select-page-elements.html#select-elements-that-contain-special-characters
            const filterTests = [
                {
                    filterCondition: '=',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: '\u003E', // https://www.toptal.com/designers/htmlarrows/math/greater-than-sign/
                    filterValue: '1',
                    columnValues: ['123', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: '\u2265', //https://www.toptal.com/designers/htmlarrows/math/greater-than-or-equal-to/
                    filterValue: '1',
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: '\u003C', //https://www.toptal.com/designers/htmlarrows/math/less-than-sign/
                    filterValue: '1',
                    columnValues: []
                },
                {
                    filterCondition: '\u2264', //https://www.toptal.com/designers/htmlarrows/math/less-than-or-equal-to/
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'B', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'B', filterTests[i].columnValues)
            }
        }
    )
});


test('Test range filter conditions, number column', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            await applyFiltersToColumn(
                t, 
                'B', 
                [
                    // Greater than 1, less than 3
                    {filterCondition: '\u003E', filterValue: '1'},
                    {filterCondition: '\u003C', filterValue: '3'},

                ]
            )
            await checkColumn(t, 'B', ['2'])
        }
    )
});

   
test('Test mulitple string contains with OR, string column', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            await applyFiltersToColumn(
                t, 
                'A', 
                [
                    {filterCondition: 'contains', filterValue: '1'},
                    {filterCondition: 'contains', filterValue: '3'},
        
                ],
                'Or'
            )
            await checkColumn(t, 'B', ['123', '1', '3'])
        }
    )
});

test('Test saves changed operators', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            await applyFiltersToColumn(
                t, 
                'A', 
                [
                    {filterCondition: 'contains', filterValue: '1'},
                    {filterCondition: 'contains', filterValue: '3'},
        
                ],
                'Or'
            )
            await checkColumn(t, 'B', ['123', '1', '3'])
        
            await applyFiltersToColumn(
                t, 
                'A', 
                [
                    {filterCondition: 'contains', filterValue: '1'},
                    {filterCondition: 'contains', filterValue: '4'},
        
                ]
            )
            await checkColumn(t, 'B', ['123', '1', '4']);
        }
    )
});

test('Test allows you to filter out NaNs', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'Name': ['Nate', 'Aaron', None]})\nmitosheet.sheet(df1)",
        async t => {

            await applyFiltersToColumn(
                t, 
                'Name', 
                [
                    {filterCondition: 'is not empty', filterValue: undefined},
                ],
            )
            await checkSheet(t, {
                'Name': ['Nate', 'Aaron']
            })

            const expectedDf = {
                'Name': ['Nate', 'Aaron']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});
   