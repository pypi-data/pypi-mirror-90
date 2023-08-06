// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import MultiToggleBox from '../../elements/MultiToggleBox';
import { SheetJSON } from '../../../widget';

import { getSuggestedColumnHeaderKeys } from './mergeUtils';

// Import 
import '../../../../css/pivot-taskpane.css'
import { TaskpaneInfo } from '../taskpanes';
import MergeSheetAndKeySelection from './MergeSheetAndKeySelection';


// Enum to allow you to refer to the first or second sheet by name, for clarity
export enum MergeSheet {
    First = 0,
    Second = 1
}


export type MergeTaskpaneProps = {
    dfNames: string[],
    sheetJSONArray: SheetJSON[],
    send: (msg: Record<string, unknown>) => void,
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
};

type MergeTaskpaneState = {
    sheetOneIndex: number,
    sheetTwoIndex: number,
    sheetOneMergeKey: string,
    sheetTwoMergeKey: string,
    sheetOneSelectedColumns: string[],
    sheetTwoSelectedColumns: string[],
    sheetOneToggleAll: boolean,
    sheetTwoToggleAll: boolean,
    originalDfNames: string[]
};

class MergeTaskpane extends React.Component<MergeTaskpaneProps, MergeTaskpaneState> {

    constructor(props: MergeTaskpaneProps) {
        super(props);

        const sheetOneIndex = 0;
        const sheetTwoIndex = Math.min(1, props.sheetJSONArray.length - 1);

        if (props.sheetJSONArray.length === 0) {
            // If there is no data, we just set default values
            this.state = {
                sheetOneIndex: sheetOneIndex,
                sheetTwoIndex: sheetTwoIndex,
                sheetOneMergeKey: '',
                sheetTwoMergeKey: '',
                sheetOneSelectedColumns: [],
                sheetTwoSelectedColumns: [],
                sheetOneToggleAll: true,
                sheetTwoToggleAll: true,
                originalDfNames: props.dfNames
            };
        } else {
            const suggestedKeys = getSuggestedColumnHeaderKeys(props.sheetJSONArray, sheetOneIndex, sheetTwoIndex);

            // We default to selecting _all_ columns
            const sheetOneSelectedColumns = [...this.props.sheetJSONArray[sheetOneIndex].columns]
            const sheetTwoSelectedColumns = [...this.props.sheetJSONArray[sheetTwoIndex].columns]
        
            this.state = {
                sheetOneIndex: sheetOneIndex,
                sheetTwoIndex: sheetTwoIndex,
                sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
                sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey,
                sheetOneSelectedColumns: sheetOneSelectedColumns,
                sheetTwoSelectedColumns: sheetTwoSelectedColumns,
                sheetOneToggleAll: true,
                sheetTwoToggleAll: true,
                originalDfNames: props.dfNames
            };

            // Send the first merge message, if there is something to send!
            this.sendMergeMessage(false);
        }

        this.setNewSheetIndex = this.setNewSheetIndex.bind(this);
        this.setNewMergeKey = this.setNewMergeKey.bind(this);
        this.toggleKeepColumnHeader = this.toggleKeepColumnHeader.bind(this);
        this.toggleAll = this.toggleAll.bind(this);
        this.sendMergeMessage = this.sendMergeMessage.bind(this);
    }


    /*
        When one of the two merge indexes is changed, we change state by:
        1. Updating the sheet index.
        2. Updating the columns that are selected (this defaults to all), as well as the toggle 
           for this sheet.
        3. Trying to find a new merge key between the sheets
    */
    setNewSheetIndex(sheetNumber: MergeSheet, newSheetIndex: number): void {
        const indexName = sheetNumber == MergeSheet.First ? 'sheetOneIndex' : 'sheetTwoIndex'
        const selectedColumnsName = sheetNumber == MergeSheet.First ? 'sheetOneSelectedColumns' : 'sheetTwoSelectedColumns';
        const toggleAllName = sheetNumber == MergeSheet.First ? 'sheetOneToggleAll' : 'sheetTwoToggleAll';

        const newSelectedColumns = [...this.props.sheetJSONArray[newSheetIndex].columns]

        this.setState(prevState => {
            // Return if we're not changing anything!
            if (prevState[indexName] == newSheetIndex) {
                return;
            }
            
            const newSuggestedKeys = getSuggestedColumnHeaderKeys(
                this.props.sheetJSONArray, 
                sheetNumber === MergeSheet.First ? newSheetIndex : prevState.sheetOneIndex, 
                sheetNumber === MergeSheet.Second ? newSheetIndex : prevState.sheetTwoIndex
            );

            return {
                ...prevState,
                [indexName]: newSheetIndex,
                [selectedColumnsName]: newSelectedColumns,
                [toggleAllName]: true,
                sheetOneMergeKey: newSuggestedKeys.sheetOneMergeKey,
                sheetTwoMergeKey: newSuggestedKeys.sheetTwoMergeKey
            }
        }, () => {
            this.sendMergeMessage();
        });
    }

    /*
        Sets a new merge key for one of the merge sheets
    */
    setNewMergeKey(sheetNumber: MergeSheet, newMergeKey: string): void {
        const mergeKeyName = sheetNumber === MergeSheet.First ? 'sheetOneMergeKey' : 'sheetTwoMergeKey';

        this.setState(prevState => {
            return {
                ...prevState,
                [mergeKeyName]: newMergeKey,
            }
        }, () => {
            this.sendMergeMessage();
        });
    }

    /*
        Toggles if we should keep a specific column at from one of the sheets in the new
        merged sheet.
    */
    toggleKeepColumnHeader(sheetNumber: MergeSheet, columnHeader: string): void {
        const selectedColumnsName = sheetNumber == MergeSheet.First ? 'sheetOneSelectedColumns' : 'sheetTwoSelectedColumns'
        const mergeKeyName = sheetNumber == MergeSheet.First ? 'sheetOneMergeKey' : 'sheetTwoMergeKey'

        this.setState(prevState => {
            // We the don't let you toggle the merge key!
            if (prevState[mergeKeyName] === columnHeader) {
                return;
            }

            const newSelectedColumns = [...prevState[selectedColumnsName]]
            if (newSelectedColumns.includes(columnHeader)) {
                newSelectedColumns.splice(newSelectedColumns.indexOf(columnHeader), 1)
            } else {
                newSelectedColumns.push(columnHeader)
            }

            return {
                ...prevState,
                [selectedColumnsName]: newSelectedColumns
            }
        }, () => {
            this.sendMergeMessage();
        });
    }

    /*
        Toggles all the check boxes selected for a given sheet, based on the current
        toggleAll state for that sheet. 
    */
    toggleAll(sheetNumber: MergeSheet): void {
        const sheetIndexName = sheetNumber === MergeSheet.First ? 'sheetOneIndex' : 'sheetTwoIndex'
        const toggleAllName = sheetNumber === MergeSheet.First ? 'sheetOneToggleAll' : 'sheetTwoToggleAll'
        const selectedColumnsName = sheetNumber === MergeSheet.First ? 'sheetOneSelectedColumns' : 'sheetTwoSelectedColumns'

        this.setState(prevState => {
            let newSelectedColumns: string[] = [];
            if (!prevState[toggleAllName]) {
                newSelectedColumns = [...this.props.sheetJSONArray[this.state[sheetIndexName]].columns]
            }
            return {
                ...prevState,
                [selectedColumnsName]: newSelectedColumns,
                [toggleAllName]: !prevState[toggleAllName]
            }
        }, () => {
            this.sendMergeMessage();
        })
    }

    /*
        Completes the merge operation by sending information for the merge
        to the backend, potentially overwriting what's already there!
    */
    sendMergeMessage(overwrite=true): void {

        // NOTE: We make sure to send the merge keys in the selected columns, no matter what
        const sheetOneSelectedColumns = [...this.state.sheetOneSelectedColumns];
        if (!sheetOneSelectedColumns.includes(this.state.sheetOneMergeKey)) {
            sheetOneSelectedColumns.push(this.state.sheetOneMergeKey)
        }
        const sheetTwoSelectedColumns = [...this.state.sheetTwoSelectedColumns];
        if (!sheetTwoSelectedColumns.includes(this.state.sheetTwoMergeKey)) {
            sheetTwoSelectedColumns.push(this.state.sheetTwoMergeKey)
        }

        window.logger?.track({
            userId: window.user_id,
            event: 'button_merge_log_event',
            properties: {
                sheet_index_one: this.state.sheetOneIndex,
                merge_key_one: this.state.sheetOneMergeKey,
                selected_columns_one: sheetOneSelectedColumns,
                sheet_index_two: this.state.sheetTwoIndex,
                merge_key_two: this.state.sheetTwoMergeKey,
                selected_columns_two: sheetTwoSelectedColumns,
                overwrite: overwrite
            }
        })

        this.props.send({
            'event': 'edit_event',
            'type': 'merge_edit',
            'sheet_index_one': this.state.sheetOneIndex,
            'merge_key_one': this.state.sheetOneMergeKey,
            'selected_columns_one': sheetOneSelectedColumns,
            'sheet_index_two': this.state.sheetTwoIndex,
            'merge_key_two': this.state.sheetTwoMergeKey,
            'selected_columns_two': sheetTwoSelectedColumns,
            overwrite: overwrite
        })
    }

    render(): JSX.Element  {
        /*
            If there is no possible merge taskpane that can be displayed (e.g. the sheetJSON is empty),
            then display this error message.
        */
        if (this.props.sheetJSONArray.length === 0) {
            return (
                <DefaultTaskpane
                    header={'Merge Sheets Together'}
                    setCurrOpenTaskpane={this.props.setCurrOpenTaskpane}
                    taskpaneBody = {
                        <Fragment>
                            Please Import data before merging.
                        </Fragment>
                    }
                />
            )
        }

        /*
            We don't let you select or unselect the sheet merge key, and note that we must account
            for the shift in the indexes that this causes when updating if the state of an item is 
            toggled.

            Thus, we filter out the merge keys from both the list of columns, as well as the 
            toggles for these columns.
        */
        const sheetOneOriginalColumns = this.props.sheetJSONArray[this.state.sheetOneIndex].columns;
        const sheetTwoOriginalColumns = this.props.sheetJSONArray[this.state.sheetTwoIndex].columns;

        const sheetOneColumns = sheetOneOriginalColumns.filter(columnHeader => columnHeader !== this.state.sheetOneMergeKey)
        const sheetTwoColumns = sheetTwoOriginalColumns.filter(columnHeader => columnHeader !== this.state.sheetTwoMergeKey)

        const sheetOneToggles = sheetOneColumns.map(columnHeader => this.state.sheetOneSelectedColumns.includes(columnHeader))
        const sheetTwoToggles = sheetTwoColumns.map(columnHeader => this.state.sheetTwoSelectedColumns.includes(columnHeader))

        return (
            <DefaultTaskpane
                header={'Merge Sheets Together'}
                setCurrOpenTaskpane={this.props.setCurrOpenTaskpane}
                taskpaneBody = {
                    <Fragment>
                        <MergeSheetAndKeySelection
                            sheetNum={MergeSheet.First}
                            dfNames={this.state.originalDfNames}
                            sheetIndex={this.state.sheetOneIndex}
                            otherSheetIndex={this.state.sheetTwoIndex}
                            setNewSheetIndex={(newSheetIndex) => {this.setNewSheetIndex(MergeSheet.First, newSheetIndex)}}
                            columnHeaders={this.props.sheetJSONArray[this.state.sheetOneIndex].columns}
                            mergeKey={this.state.sheetOneMergeKey}
                            setNewMergeKey={(newMergeKey) => this.setNewMergeKey(MergeSheet.First, newMergeKey)}
                        />
                        <div className='mb-25px'>
                            <p className='default-taskpane-body-section-title-text'>
                                Columns to Keep
                            </p>
                            <MultiToggleBox
                                itemsArray={sheetOneColumns}
                                itemToggleState={sheetOneToggles}
                                toggleItemAtIndex={(index: number) => this.toggleKeepColumnHeader(MergeSheet.First, sheetOneColumns[index])}
                                toggleAllOptions={{
                                    currentToggleAllState: this.state.sheetOneToggleAll,
                                    toggleAll: () => {this.toggleAll(MergeSheet.First)}
                                }}
                            />
                        </div>
                        <MergeSheetAndKeySelection
                            sheetNum={MergeSheet.Second}
                            dfNames={this.state.originalDfNames}
                            sheetIndex={this.state.sheetTwoIndex}
                            otherSheetIndex={this.state.sheetOneIndex}
                            setNewSheetIndex={(newSheetIndex) => {this.setNewSheetIndex(MergeSheet.Second, newSheetIndex)}}
                            columnHeaders={this.props.sheetJSONArray[this.state.sheetTwoIndex].columns}
                            mergeKey={this.state.sheetTwoMergeKey}
                            setNewMergeKey={(newMergeKey) => this.setNewMergeKey(MergeSheet.Second, newMergeKey)}
                        />
                        <div>
                            <p className='default-taskpane-body-section-title-text'>
                                Columns to Keep
                            </p>
                            <MultiToggleBox
                                itemsArray={sheetTwoColumns}
                                itemToggleState={sheetTwoToggles}
                                toggleItemAtIndex={(index: number) => this.toggleKeepColumnHeader(MergeSheet.Second, sheetTwoColumns[index])}
                                toggleAllOptions={{
                                    currentToggleAllState: this.state.sheetTwoToggleAll,
                                    toggleAll: () => {this.toggleAll(MergeSheet.Second)}
                                }}
                            />
                        </div>
                    </Fragment>
                }
            />
        )
    }
}

export default MergeTaskpane;