import { Reducer } from "redux";
import { RootStateMaybe } from "..";

export const ADD_PROGRAM: string = 'ADD_PROGRAM';
export const ADD_TESTCASE: string = 'ADD_TESTCASE';

export const REMOVE_PROGRAM: string = 'REMOVE_PROGRAM';
export const REMOVE_TESTCASE: string = 'REMOVE_TESTCASE';

export const INCR_PROGRAM: string = 'INCR_PROGRAM';
export const INCR_TESTCASE: string = 'INCR_TESTCASE';

export const CHANGE_VIEW: string = 'CHANGE_VIEW';


export interface DispatchRequest {
    type: string,
    payload?: any
}

function insert( array: any, index: number, item: any ) {
    array[index-1] = item;
};

export const storeReducer: Reducer<RootStateMaybe, DispatchRequest> = (state: any, action: DispatchRequest) => {

    if (state !== undefined && action.hasOwnProperty('type')) {
        
        console.log('reducer: ',action);
        let copyState: RootStateMaybe = { ...state };

        switch (action.type) {
            case ADD_PROGRAM:
                insert(copyState.programs, action.payload.position, action.payload.text);
                break;


            case ADD_TESTCASE:
                insert(copyState.testcases, action.payload.position, action.payload.text);
                break;

            case REMOVE_PROGRAM:
                insert(copyState.programs, action.payload, null);
                break;

            case REMOVE_TESTCASE:
                insert(copyState.testcases, action.payload, null);
                break;

            case INCR_PROGRAM:
                console.log('ou');
                copyState.programsNumber++;
                break;

            case INCR_TESTCASE:
                copyState.testsNumber++;
                break;

            case CHANGE_VIEW:
                copyState.view = {...action.payload};
                break
        }
        console.log(state);
        return copyState;
    }
    return state;
}