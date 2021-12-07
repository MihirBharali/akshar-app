export default {
  namespaced: true,
  state: {
    classrooms: [],
    notifications: [],
    matchups: [],
  },
  mutations: {
    SET_LEARNER_CLASSROOMS(state, classrooms) {
      state.classrooms = [...classrooms];
    },
    SET_LEARNER_NOTIFICATIONS(state, notifications) {
      state.notifications = notifications;
    },
    SET_MATCHUP_DATA(state, matchups) {
      state.matchups = matchups;
    },
    RESET_STATE(state) {
      state.classrooms = [];
      state.notifications = [];
      state.matchups = [];
    },
  },
};
