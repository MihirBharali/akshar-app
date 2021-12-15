import * as actions from './actions';

export default {
  namespaced: true,
  state: {
    facilityWageRequests: [],
    learners: [],
    facilityAllWageRequests: [],
    facilityAllLearnersRequests: [],
    defaultStartDate: null,
    defaultEndDate: null,
  },
  mutations: {
    SET_FACILITY_WAGE_DETAILS(state, { facilityWageRequests, learners }) {
      state.facilityWageRequests = facilityWageRequests;
      state.learners = learners;
    },
    SET_FACILITY_WAGE_DETAILS_FOR_REPORTING(
      state,
      { facilityAllWageRequests, defaultStartDate, defaultEndDate }
    ) {
      state.facilityAllWageRequests = facilityAllWageRequests;
      state.facilityAllLearnersRequests = facilityAllWageRequests;
      state.defaultStartDate = defaultStartDate;
      state.defaultEndDate = defaultEndDate;
    },
    UPDATE_CONSOLIDATED_CHART_WAGE_DETAILS(state, { facilityAllWageRequests }) {
      state.facilityAllWageRequests = facilityAllWageRequests;
    },
    UPDATE_LEARNERS_CHART_WAGE_DETAILS(state, { facilityAllWageRequests }) {
      state.facilityAllLearnersRequests = facilityAllWageRequests;
    },
    UPDATE_FACILITY_WAGE_REQUEST_LIST(state, newTxn) {
      state.facilityWageRequests.push(newTxn);
    },
    RESET_STATE(state) {
      state.facilityWageRequests = [];
      state.learners = [];
    },
  },
  actions,
};
