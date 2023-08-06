// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import {
    tryTest,
} from '../utils/helpers';

const code = `
import mitosheet
mitosheet.sheet()
`
import { CURRENT_URL } from '../config';
import { documentationButton, documentationTaskpaneBackButton, documentationTaskpaneCloseButton, documentationTaskpaneFunctionSelector } from '../utils/selectors';

fixture `Test Documentation`
    .page(CURRENT_URL)

test('Allows for a interaction with the documentation', async t => {
    tryTest(
        t,
        code,
        async t => {
            // open docuemntation taskpane
            await t.click(documentationButton);

            // click on the first documentation list item
            await t.click(documentationTaskpaneFunctionSelector);

            // use the back button
            await t.click(documentationTaskpaneBackButton);

            // close the documentation taskpane
            await t.click(documentationTaskpaneCloseButton);
        }
    )
});
