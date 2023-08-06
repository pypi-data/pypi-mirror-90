// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { SheetShape } from '../../widget';
import SheetTab from './SheetTab';

// import css
import "../../../css/sheet-tab.css"

type SheetTabsProps = {
    mitoContainerRef: HTMLDivElement | undefined | null;
    send: (msg: Record<string, unknown>) => void;
    dfNames: string[];
    sheetShapeArray: SheetShape[];
    selectedSheetIndex: number;
    setSelectedSheetIndex: (newIndex: number) => void;
    closeEditingTaskpane: () => void;
};

/*
    Wrapper component that displays the entire bottom of the sheet, including
    the sheet tabs, as well as the shape of the currently selected dataframe.
*/
function SheetTabs(props: SheetTabsProps): JSX.Element {
    return (
        <div className='sheet-bottom'>
            <div className="sheet-tab-bar">
                {props.dfNames.map((dfName, idx) => {
                    return (
                        <SheetTab
                            key={idx}
                            mitoContainerRef={props.mitoContainerRef}
                            send={props.send}
                            dfName={dfName}
                            sheetShape={props.sheetShapeArray[idx]}
                            sheetIndex={idx}
                            selectedSheetIndex={props.selectedSheetIndex}
                            setSelectedSheetIndex={props.setSelectedSheetIndex}
                            closeEditingTaskpane={props.closeEditingTaskpane}
                        />
                    )
                })}
            </div>
            {props.sheetShapeArray[props.selectedSheetIndex] !== undefined && 
                <div className='sheet-shape'>
                    ({props.sheetShapeArray[props.selectedSheetIndex].rows}, {props.sheetShapeArray[props.selectedSheetIndex].cols})
                </div>
            }
        </div>
    );
}

export default SheetTabs;
