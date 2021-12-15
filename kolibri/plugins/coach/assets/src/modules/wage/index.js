import * as actions from './actions';

export default {
  namespaced: true,
  state: {
    coachWageRequests: [],
    learners: [],
  },
  mutations: {
    SET_COACH_WAGE_REQUEST_LIST(state, { coachWageRequests, learners }) {
      state.coachWageRequests = coachWageRequests;
      state.learners = learners;
    },
    UPDATE_COACH_WAGE_REQUEST_LIST(state, { data, add }) {
      if (add) {
        state.coachWageRequests.push(data);
      }
      state.coachWageRequests = state.coachWageRequests.filter(item => !data.includes(item['id']));
    },
    RESET_STATE(state) {
      state.coachWageRequests = [];
      state.learners = [];
    },
  },
  actions,
};
