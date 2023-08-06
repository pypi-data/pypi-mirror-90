// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import {
    getColumnHeaderNameSelector,
    getColumnHeaderContainerSelector
} from '../utils/columnHelpers'


import {
    columnHeaderChangeInputSelector,
    columnHeaderChangeErrorSelector,
} from '../utils/selectors';

import { 
    modalSelector,
    modalHeaderSelector,
    modalAdvanceButtonSelector
} from '../utils/allModals';

import { 
    tryTest,
    DELETE_PRESS_KEYS_STRING
} from '../utils/helpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

const code = 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [101, 102, 103]})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [201, 202, 203]})\nmitosheet.sheet(df1, df2)';

fixture `Test Rename Column Headers`
    .page(CURRENT_URL)

test('Allows you to rename to valid headers only', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t
                .click(getColumnHeaderNameSelector('id'))
                .expect(modalSelector.exists).ok()
                .expect(modalHeaderSelector.innerText).contains('Change Column Name: id')
                .expect(modalAdvanceButtonSelector.innerText).eql('Change Column Name')

            // Enter some invalid headers, and get error messages
            await t
                .typeText(columnHeaderChangeInputSelector, "123")
                .expect(columnHeaderChangeErrorSelector.exists).ok()
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(columnHeaderChangeInputSelector, "h a")
                .expect(columnHeaderChangeErrorSelector.exists).ok()
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(columnHeaderChangeInputSelector, "h-a")
                .expect(columnHeaderChangeErrorSelector.exists).ok()
                .pressKey(DELETE_PRESS_KEYS_STRING)
            
            // Finially, change to a valid header, and make sure the change goes through
            await t
                .typeText(columnHeaderChangeInputSelector, "h_a")
                .expect(columnHeaderChangeErrorSelector.exists).notOk()
                .click(modalAdvanceButtonSelector)
                .expect(getColumnHeaderContainerSelector('h_a').exists).ok()

            const expectedDf = {
                'h_a': ['1', '2', '3'],
                'values': ['101', '102', '103']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});
   