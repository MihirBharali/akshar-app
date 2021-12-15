import * as actions from './actions';

export default {
  namespaced: true,
  state: {
    wagedetails: [],
  },
  mutations: {
    SET_LEARNER_WAGE_DETAILS(state, wagedetails) {
      state.wagedetails = wagedetails;
    },
    UPDATE_LEARNER_WAGE_DETAILS(state, newTxn) {
      state.wagedetails['transactions'].push(newTxn);
    },
    RESET_STATE(state) {
      state.wagedetails = [];
    },
  },
  actions,
};
