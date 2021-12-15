import { WageTransactionResource, FacilityUserResource } from 'kolibri.resources';
import ConditionalPromise from 'kolibri.lib.conditionalPromise';
import samePageCheckGenerator from 'kolibri.utils.samePageCheckGenerator';
import { PageNames } from '../../constants';

export function showCoachWagePage(store) {
  store.dispatch('loading');
  const facilityId = store.getters.activeFacilityId;
  const promises = [
    WageTransactionResource.fetchCollection({
      getParams: { role: 'Coach' },
      force: true,
    }),
    FacilityUserResource.fetchCollection({ getParams: { member_of: facilityId }, force: true }),
  ];

  ConditionalPromise.all(promises).only(
    samePageCheckGenerator(store),
    ([transactions, facilityUsers]) => {
      const learners = facilityUsers.filter(item => item['roles'].length == 0);
      store.commit('wage/SET_COACH_WAGE_REQUEST_LIST', {
        coachWageRequests: transactions,
        learners: learners,
      });
      store.commit('SET_PAGE_NAME', PageNames.COACH_WAGE_REQUEST_LIST_PAGE);
      store.dispatch('clearError');
      store.dispatch('notLoading');
    },
    error => {
      store.dispatch('handleError', error);
    }
  );
}
