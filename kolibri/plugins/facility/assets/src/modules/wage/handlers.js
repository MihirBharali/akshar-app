import { WageTransactionResource, FacilityUserResource } from 'kolibri.resources';
import ConditionalPromise from 'kolibri.lib.conditionalPromise';
import samePageCheckGenerator from 'kolibri.utils.samePageCheckGenerator';

export function showWageDetailsPage(store) {
  store.dispatch('loading');
  const facilityId = store.getters.activeFacilityId;
  const promises = [
    WageTransactionResource.fetchCollection({
      getParams: { role: 'Admin', facility: facilityId },
      force: true,
    }),
    FacilityUserResource.fetchCollection({ getParams: { member_of: facilityId }, force: true }),
  ];

  ConditionalPromise.all(promises).only(
    samePageCheckGenerator(store),
    ([transactions, facilityUsers]) => {
      const learners = facilityUsers.filter(item => item['roles'].length == 0);
      store.commit('wage/SET_FACILITY_WAGE_DETAILS', {
        facilityWageRequests: transactions,
        learners: learners,
      });
      store.commit('CORE_SET_PAGE_LOADING', false);
      store.dispatch('clearError');
      store.dispatch('notLoading');
    },
    error => {
      store.dispatch('handleApiError', error);
      store.commit('CORE_SET_PAGE_LOADING', false);
    }
  );
}

export function showWageReportingPage(store) {
  const today = new Date();
  let dd = String(today.getDate()).padStart(2, '0');
  let mm = String(today.getMonth() + 1).padStart(2, '0');
  let yyyy = today.getFullYear();
  let startDate = yyyy + '-' + mm + '-01';
  let endDate = yyyy + '-' + mm + '-' + dd;

  WageTransactionResource.fetchCollection({
    getParams: {
      type: 'Reporting',
      status: 'COMPLETED',
      startDate: startDate,
      endDate: endDate,
      facility: store.getters.activeFacilityId,
    },
    force: true,
  })
    .then(transactions => {
      store.commit('wage/SET_FACILITY_WAGE_DETAILS_FOR_REPORTING', {
        facilityAllWageRequests: transactions,
        defaultStartDate: startDate,
        defaultEndDate: endDate,
      });
      store.commit('CORE_SET_PAGE_LOADING', false);
      store.dispatch('clearError');
      store.dispatch('notLoading');
    })
    .catch(err => {
      store.dispatch('handleApiError', err);
      store.commit('CORE_SET_PAGE_LOADING', false);
    });
}
