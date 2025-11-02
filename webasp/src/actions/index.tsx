import {
    ADD_PROGRAM,
    ADD_TESTCASE,
    DispatchRequest,
    INCR_PROGRAM,
    INCR_TESTCASE,
    REMOVE_PROGRAM,
    REMOVE_TESTCASE,
    CHANGE_VIEW
} from '../reducer';

export const changeView = (type: string, number: number) => {
    return {
        type: CHANGE_VIEW,
        payload:{
            type: type,
            num: number
        }
    }
}

export const addProgram = (text: string | undefined, isTest: boolean, position: number): DispatchRequest => {
    return {
        type: isTest? ADD_TESTCASE: ADD_PROGRAM,
        payload:{text, position}
    };
}

export const addViewProgram = (isTest: boolean): DispatchRequest => {
    return{
        type: isTest? INCR_TESTCASE: INCR_PROGRAM
    };
}

export const clearProgram = (isTest: boolean, position: number): DispatchRequest => {
    return {
        type: isTest ? REMOVE_TESTCASE : REMOVE_PROGRAM,
        payload: position
    };
}