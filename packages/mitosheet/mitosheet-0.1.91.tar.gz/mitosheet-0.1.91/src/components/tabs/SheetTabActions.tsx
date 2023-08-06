// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../../css/sheet-tab.css"

/*
    Displays a set of actions one can perform on a sheet tab, including
    deleting, duplicating, or renaming.
*/
export default function SheetTabActions(props: {
    setDisplayActions: React.Dispatch<React.SetStateAction<boolean>>;
    setIsRename: React.Dispatch<React.SetStateAction<boolean>>;
    send: (msg: Record<string, unknown>) => void,
    dfName: string, 
    sheetIndex: number,
    getLeftShift: () => number
}): JSX.Element {

    const onDelete = (): void => {
        window.logger?.track({
            userId: window.user_id,
            event: 'dataframe_delete_log_event',
            properties: {
                sheet_index: props.sheetIndex,
                old_dataframe_name: props.dfName
            }
        })

        props.send({
            'event': 'edit_event',
            'type': 'dataframe_delete_edit',
            'sheet_index': props.sheetIndex,
        })

        props.setDisplayActions(false);
    }

    const onDuplicate = (): void => {
        window.logger?.track({
            userId: window.user_id,
            event: 'dataframe_duplicate_log_event',
            properties: {
                sheet_index: props.sheetIndex,
                old_dataframe_name: props.dfName
            }
        })

        props.send({
            'event': 'edit_event',
            'type': 'dataframe_duplicate_edit',
            'sheet_index': props.sheetIndex,
        })

        props.setDisplayActions(false);
    }

    /* Rename helper, which requires changes to the sheet tab itself */
    const onRename = (): void => {
        props.setDisplayActions(false);
        props.setIsRename(true);
    }

    return (
        <div className='sheet-tab-actions-dropdown' style={{left: props.getLeftShift()}}>
            {/* NOTE: we shift with the location of the actions, so it is placed properly */}
            <div className='sheet-tab-action' onClick={onDelete}>
                Delete
            </div>
            <div className='sheet-tab-action' onClick={onDuplicate}>
                Duplicate
            </div >
            <div className='sheet-tab-action' onClick={onRename}>
                Rename
            </div>
        </div>
    )
}
