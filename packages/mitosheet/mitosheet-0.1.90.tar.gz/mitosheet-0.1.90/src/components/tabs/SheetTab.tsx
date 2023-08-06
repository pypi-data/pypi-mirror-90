// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useRef } from 'react';
import { SheetShape } from '../../widget';
import SheetTabActions from './SheetTabActions';

// import css
import "../../../css/sheet-tab.css"

type SheetTabProps = {
    mitoContainerRef: HTMLDivElement | undefined | null;
    send: (msg: Record<string, unknown>) => void;
    dfName: string;
    sheetShape: SheetShape;
    sheetIndex: number;
    selectedSheetIndex: number;
    setSelectedSheetIndex: (newIndex: number) => void;
    closeEditingTaskpane: () => void;
};

/*
    Component that displays a dataframe name at the bottom of the sheet, and
    furthermore renders the sheet actions if the sheet action dropdown is 
    clicked.
*/
export default function SheetTab(props: SheetTabProps): JSX.Element {

    const [displayActions, setDisplayActions] = useState<boolean>(false);
    const [isRename, setIsRename] = useState<boolean>(false);
    const [newDataframeName, setNewDataframeName] = useState<string>(props.dfName);
    const selectedClass = props.selectedSheetIndex == props.sheetIndex ? 'selected-tab' : '';
    
    const elRef = useRef<HTMLDivElement>(null);

    /*
        Helper function that determines how much we should shift the SheetTabActions over.

        To do so, we find the bounding box of the Mito container as well as the tab itself. 
        The bounding box can be understood as the left, right, top and bottom pixel indexes
        of the div element itself. 

        We return the difference between the left edge of the mito container as well as the 
        tab. However, we cap this at 1, so that the SheetTabActions must be displayed within
        the Mito container.
    */
    function getLeftShift(): number {
        const containerRectLeft = elRef.current?.getBoundingClientRect()?.left;
        const tabRectLeft = props.mitoContainerRef?.getBoundingClientRect()?.left;
        if (containerRectLeft && tabRectLeft) {
            return Math.max(containerRectLeft - tabRectLeft, 1);
        }
        return 0;
    }

    const onRename = (): void => {
        window.logger?.track({
            userId: window.user_id,
            event: 'dataframe_rename_log_event',
            properties: {
                sheet_index: props.sheetIndex,
                new_dataframe_name: newDataframeName,
                old_dataframe_name: props.dfName
            }
        })

        props.send({
            'event': 'edit_event',
            'type': 'dataframe_rename_edit',
            'sheet_index': props.sheetIndex,
            'new_dataframe_name': newDataframeName
        })

        setDisplayActions(false);
        setIsRename(false);
    }

    const toggleSheetTabActions = () => {
        props.closeEditingTaskpane();
        setDisplayActions(!displayActions);
    }

    return (
        <div ref={elRef} className={'tab' + ' ' + selectedClass} onClick={() => {props.setSelectedSheetIndex(props.sheetIndex)}}>
            <div className='tab-text'>
                {isRename && 
                    <form onSubmit={(e) => {e.preventDefault(); onRename()}}>
                        <input 
                            type='text'
                            value={newDataframeName} 
                            onChange={(e) => {setNewDataframeName(e.target.value)}}
                            autoFocus
                        />
                    </form>
                }
                {!isRename &&
                    <p className='tab-sheet-name'>
                        {props.dfName} 
                    </p>
                }
                {/* Display the dropdown that allows a user to perform some action */}
                <svg onClick={toggleSheetTabActions} width="15" height="20" viewBox="0 0 9 4" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.50098 4L8.39809 0.25H0.603862L4.50098 4Z" fill="#C4C4C4"/>
                </svg>
            </div>
            {displayActions && 
                <SheetTabActions 
                    setDisplayActions={setDisplayActions}
                    setIsRename={setIsRename}
                    send={props.send}
                    dfName={props.dfName}
                    sheetIndex={props.sheetIndex} 
                    getLeftShift={getLeftShift}
                />
            }
        </div>
    );
}
