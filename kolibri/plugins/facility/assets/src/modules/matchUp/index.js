import { getMatchupData, saveMatchupData } from './actions';

function defaultState() {
  return {
    matchupData: {},
    originalMatchupData: {},
  };
}

export default {
  namespaced: true,
  state: defaultState(),
  mutations: {
    SET_MATCH_UP_DATA(state, payload) {
      Object.assign(state, { matchupData: payload, originalMatchupData: payload });
    },
  },
  actions: {
    getMatchupData,
    saveMatchupData,
  },
};
