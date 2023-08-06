// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import { SheetJSON } from '../../../widget';
import LargeSelect from '../../elements/LargeSelect';
import PivotTableKeySelection from './PivotTableKeySelection';

// Import 
import '../../../../css/pivot-taskpane.css'
import PivotTableValueSelection from './PivotTableValueSelection';
import { TaskpaneInfo } from '../taskpanes';


// The aggregation functions we're supporting, out of the box
export enum AggregationType {
    SUM = 'sum',
    MEAN = 'mean',
    MEDIAN = 'median',
    MIN = 'min',
    MAX = 'max', 
    COUNT = 'count', 
    STD = 'std',
}

export enum KeyType {
    Row = 'Row',
    Col = 'Col',
}

export enum SelectionOperation {
    ADD = 'Add',
    REMOVE = 'Remove'
}

export type PivotTaskpaneProps = {
    sheetJSONArray: SheetJSON[];
    dfNames: string[];
    send: (msg: Record<string, unknown>) => void,
    selectedSheetIndex: number
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void;
};

type PivotTaskpaneState = {
    dfNames: string[],
    selectedSheetIndex: number,
    selectedGroupByRows: string[],
    selectedGroupByCols: string[],
    values: Record<string, AggregationType>, // Mapping from column header to aggregation type
    keyError: string, 
};


class PivotTaskpane extends React.Component<PivotTaskpaneProps, PivotTaskpaneState> {

    constructor(props: PivotTaskpaneProps) {
        super(props);
    
        this.state = {
            dfNames: this.props.dfNames,
            selectedSheetIndex: props.selectedSheetIndex,
            selectedGroupByRows: [],
            selectedGroupByCols: [],
            values: {},
            keyError: '', 
        };

        this.getSelectableKeyColumnHeaders = this.getSelectableKeyColumnHeaders.bind(this);
        this.editValueAggregationSelection = this.editValueAggregationSelection.bind(this);
        this.sendPivotTableUpdateMessage = this.sendPivotTableUpdateMessage.bind(this);

        // If there is any data to pivot, create a new blank sheet for this pivot table
        if (props.sheetJSONArray.length !== 0) {
            this.sendPivotTableUpdateMessage(false)
        }
    }

    editValueAggregationSelection = (columnHeader: string, operation: SelectionOperation, aggregationType?: AggregationType): void => {

        this.setState(prevState => {
            const newValues = JSON.parse(JSON.stringify(prevState.values));
            if (operation == SelectionOperation.ADD && aggregationType) {
                // If the column is being added as a new aggregated value, add it
                newValues[columnHeader] = aggregationType
            } else if (operation == SelectionOperation.REMOVE) {
                // If the column is being removed as an aggregated value, remove it
                delete newValues[columnHeader];
            }
            return {
                values: newValues
            }
        }, () => {
            this.sendPivotTableUpdateMessage()
        });    
    }   

    /* 
        A callback used by the select data source Select Element so that it can 
        set the state of the Pivot Table Taskpane
    */ 
    setSelectedSheet = (newSheetName: string): void => {
        const newSelectedSheetIndex = this.state.dfNames.indexOf(newSheetName)

        // If you didn't select a new sheet, then don't do clear your selections
        if (newSelectedSheetIndex == this.state.selectedSheetIndex) {
            return;
        }
        /* 
            Reset the keys so 
                1) the column headers currently selected are dropped 
                2) the values currently aggregated are dropped
                3) display the column headers from the new sheet
        */ 
        this.setState({
            selectedSheetIndex: newSelectedSheetIndex,
            selectedGroupByRows: [],
            selectedGroupByCols: [],
            values: {}
        });
    }

    // Function used to add/remove column headers to the row and column keys 
    editKeySelection = (keyType: KeyType, columnHeader: string, operation:  SelectionOperation): void =>  {
        // Sanity check: make sure that this column is not already selected. this should not be possible!
        if (operation === SelectionOperation.ADD) {
            if (this.state.selectedGroupByRows.includes(columnHeader) || this.state.selectedGroupByCols.includes(columnHeader)) {
                console.log("column selected as key twice in pivot table. should not be possible");
                return;
            }
        }

        this.setState(prevState => {
            let previousColumnHeaders: string[] = [];
            if (keyType === KeyType.Row) {
                previousColumnHeaders = [...prevState.selectedGroupByRows]
            } else {
                previousColumnHeaders = [...prevState.selectedGroupByCols]
            }

            if (operation == SelectionOperation.ADD && !previousColumnHeaders.includes(columnHeader)) {
                // If the operation was add, add the column header to the list of column headers (if not already included)
                previousColumnHeaders.push(columnHeader)
            } else if (operation == SelectionOperation.REMOVE && previousColumnHeaders.includes(columnHeader)) {
                // If the operation was remove, add the column header to the list of column headers (if not already included)
                previousColumnHeaders.splice(previousColumnHeaders.indexOf(columnHeader), 1)
            }

            return {
                ...prevState,
                [keyType === KeyType.Row ? 'selectedGroupByRows' : 'selectedGroupByCols']: previousColumnHeaders
            }
        }, () => {
            this.sendPivotTableUpdateMessage()
        })
    }

    /*
        Completes the group operation by sending information for the group
        to the backend.
    */
    sendPivotTableUpdateMessage = (overwrite = true): void => {
        // Log
        window.logger?.track({
            userId: window.user_id,
            event: 'button_pivot_log_event',
            properties: {
                sheet_index: this.state.selectedSheetIndex,
                pivot_rows: this.state.selectedGroupByRows,
                pivot_cols: this.state.selectedGroupByCols,
                values: this.state.values,
                overwrite: overwrite
            }
        })

        this.props.send({
            'event': 'edit_event',
            'type': 'pivot_edit',
            sheet_index: this.state.selectedSheetIndex,
            pivot_rows: this.state.selectedGroupByRows,
            pivot_columns: this.state.selectedGroupByCols,
            values: this.state.values, 
            overwrite: overwrite
        });
    }

    /* 
        Returns the remaining possible column header keys. 
        A column header can only be used in either the row or column key
    */ 
    getSelectableKeyColumnHeaders(): string[] {
        const allColumnHeaders: string[] = this.props.sheetJSONArray[this.state.selectedSheetIndex].columns
        return allColumnHeaders.filter(x => !this.state.selectedGroupByRows.includes(x) && !this.state.selectedGroupByCols.includes(x));
    }

    render(): JSX.Element  {
        /*
            If there is no possible Pivot taskpane that can be displayed (e.g. the sheetJSON is empty),
            give an error message indicating so.
        */
        if (this.props.sheetJSONArray.length === 0) {
            return (
                <DefaultTaskpane
                    header={'Create a Pivot Table'}
                    setCurrOpenTaskpane={this.props.setCurrOpenTaskpane}
                    taskpaneBody = {
                        <Fragment>
                            Please Import data before pivoting.
                        </Fragment>
                    }
                />
            )
        }


        const selectableColumnHeaders = this.getSelectableKeyColumnHeaders()
        const groupByRows = this.state.selectedGroupByRows;
        const groupByCols = this.state.selectedGroupByCols;
        
        return (
            <DefaultTaskpane
                header={'Create a Pivot Table'}
                setCurrOpenTaskpane={this.props.setCurrOpenTaskpane}
                taskpaneBody = {
                    <Fragment>
                        <div className = 'default-taskpane-body-section-div pivot-taskpane-section-header-div'>
                            <p className='default-taskpane-body-section-title-text'>
                                Data Source
                            </p>
                            <LargeSelect
                                startingValue={this.state.dfNames[this.state.selectedSheetIndex]}
                                key={this.state.selectedSheetIndex} // To update the display when you change selections
                                optionsArray={this.state.dfNames}
                                setValue={this.setSelectedSheet}
                            />
                        </div>
                        <div className = 'default-taskpane-body-section-div'>
                            <PivotTableKeySelection
                                sectionTitle={'Rows'}
                                selectableColumnHeaders={selectableColumnHeaders}
                                selectedColumnHeaders={groupByRows}
                                editKeySelection={this.editKeySelection}
                                keyType={KeyType.Row}
                            />
                        </div>
                        <div className = 'default-taskpane-body-section-div'>
                            <PivotTableKeySelection
                                sectionTitle={'Columns'}
                                selectableColumnHeaders={selectableColumnHeaders}
                                selectedColumnHeaders={groupByCols}
                                editKeySelection={this.editKeySelection}
                                keyType={KeyType.Col}
                            />
                        </div>
                        <div className='default-taskpane-body-section-div'>
                            <PivotTableValueSelection
                                columnHeaders={this.props.sheetJSONArray[this.state.selectedSheetIndex].columns}
                                aggregatedValuesInSection={this.state.values}
                                editValueAggregationSelection={this.editValueAggregationSelection}
                            />
                        </div>
                    </Fragment>
                }
            />
        ); 
    }
}

export default PivotTaskpane;