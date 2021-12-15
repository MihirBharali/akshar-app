<template>

  <KPageContainer>
    <KGrid>
      <KGridItem
        :layout8="{ span: 4 }"
        :layout12="{ span: 6 }"
      >
        <h2>{{ $tr('yourRequestsLabel') }}</h2>
        <p> {{ $tr('yourRequestsSubheader') }} </p>
      </KGridItem>
      <KGridItem
        :layout="{ alignment: 'right' }"
        :layout8="{ span: 4 }"
        :layout12="{ span: 6 }"
      >
        <KButton
          :primary="true"
          class="move-down"
          @click="showCreateFormModal = true"
        >
          {{ $tr('newRequest') }}
        </KButton>
      </KGridItem>
    </KGrid>
    <PaginatedListContainer
      v-if="hasTransactions"
      :items="filterTransactionByStatus"
      :itemsPerPage="10"
      :filterPlaceholder="$tr('searchboxPlaceholderText')"
    >
      <template #otherFilter>
        <KSelect
          v-model="statusFilter"
          label="Status"
          :options="listOfStatuses"
          :inline="true"
          class="type-filter"
        />
      </template>
      <template #default="{ items }">
        <CoreTable
          :selectable="true"
          :emptyMessage="$tr('searchNoResultText')"
        >   
          <template #headers>
            <th class="table-header">
              {{ $tr('transactionId') }}
            </th>
            <th class="table-header">
              {{ $tr('learner') }}
            </th>
            <th class="table-header">
              {{ $tr('date') }}
            </th>
            <th class="table-header">
              {{ $tr('amount') }}
            </th>
            <th class="table-header">
              {{ $tr('reason') }}
            </th>
            <th class="table-header">
              {{ $tr('status') }}
            </th>
          </template>  
          <template #tbody>
            <tbody>
              <tr v-for="txn in items" :key="txn.id">
                <td class="table-data">
                  {{ txn.id }}
                </td>
                <td class="table-data">
                  {{ txn.user_name }}
                </td>
                <td class="table-data">
                  {{ txn.transaction_date }}
                </td>
                <td class="table-data">
                  {{ txn.transaction_amount }}
                </td>
                <td class="table-data">
                  <template v-if="txn.description != undefined">
                    <KIcon 
                      :ref="toolKitReference(txn.id)"
                      icon="infoPrimary"
                      class="item svg-item"
                    />
                    <KTooltip
                      :reference="toolKitReference(txn.id)" 
                      :refs="$refs"
                      placement="bottom"
                    >
                      {{ txn.description }}
                    </KTooltip>

                  </template>  
                  {{ txn.reason }}
                </td>
                <td class="table-data">
                  {{ txn.status }}
                </td>


              </tr>
            </tbody>
          </template>  
        </CoreTable>
      </template>
    </PaginatedListContainer>  
    <div v-else>
      {{ $tr('noRequests') }}
    </div>  



    <CoachWageFormModal  
      v-if="showCreateFormModal" 
      @submit="createWageRequest" 
      @cancel="showCreateFormModal = false"
    />
    <KModal
      v-if="showErrorModal"
      :title="$tr('errorModalTitle')"
      :submitText="$tr('submitLabel')"
      @submit="showErrorModal = false"
    >
      <KLabeledIcon icon="error" :color="$themeTokens.error">
        {{ errorMessage }}
      </KLabeledIcon>  
    </KModal>
  </KPageContainer>

</template>
<script>

  import { mapState } from 'vuex';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import PaginatedListContainer from 'kolibri.coreVue.components.PaginatedListContainer';
  import filterTransactionsByStatusType from 'kolibri.utils.filterTransactionsByStatusType';
  import {
    WageStatusesDropdownOptions,
    DefaultSelectedWageTxnStatus,
  } from 'kolibri.coreVue.vuex.constants';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import _reduce from 'lodash/reduce';
  import _find from 'lodash/find';
  import CoachWageFormModal from './CoachWageFormModal.vue';

  export default {
    name: 'CoachRequestsBlock',
    components: { PaginatedListContainer, CoreTable, CoachWageFormModal },
    mixins: [commonCoreStrings],
    data() {
      return {
        showCreateFormModal: false,
        listOfStatuses: [],
        transactions: [],
        statusFilter: null,
        hasTransactions: false,
        showErrorModal: false,
        errorMessage: null,
      };
    },
    computed: {
      ...mapState('wage', ['coachWageRequests']),
      filterTransactionByStatus() {
        return filterTransactionsByStatusType(this.transactions, this.statusFilter.value);
      },
    },
    beforeMount() {
      this.init();
    },
    methods: {
      createWageRequest({ name, id, amount, requestType, reason, description }) {
        this.$store
          .dispatch('wage/createWageTransactionForLearnerRequest', {
            amount: amount,
            requestType: requestType,
            reason: reason,
            user_id: id,
            user_name: name,
            description: description,
            facility: this.$store.getters.currentFacilityId,
          })
          .then(response => {
            this.showSnackbarNotification('wageTxnCreatedSuccessMessage');
            this.$store.commit('wage/UPDATE_COACH_WAGE_REQUEST_LIST', {
              data: response,
              add: true,
            });
            this.sortTransactions();
          })
          .catch(err => {
            if (err.response != undefined && err.response.data.code === 100) {
              this.errorMessage = err.response.data.message;
              this.showErrorModal = true;
            } else {
              this.$store.dispatch('handleApiError', err);
            }
          });
        this.showCreateFormModal = false;
      },
      init() {
        this.listOfStatuses = Object.values(WageStatusesDropdownOptions);
        this.statusFilter = DefaultSelectedWageTxnStatus;
        this.sortTransactions();
        this.hasTransactions = Object.keys(this.transactions).length > 0;
      },
      sortTransactions() {
        this.transactions = this.coachWageRequests.filter(
          item => item['created_by_id'] == this.$store.getters.currentUserId
        );
        this.transactions = this.transactions.sort((a, b) => (a.id < b.id ? 1 : -1));
      },
      toolKitReference(id) {
        return 'icon__' + id;
      },
    },
    $trs: {
      yourRequestsLabel: 'Your requests',
      yourRequestsSubheader: 'Requests raised by you for your students',
      noRequests: "You don't have any requests right now.",
      newRequest: 'New request',
      searchboxPlaceholderText: 'Search for transactions..',
      searchNoResultText: 'No matching transactions found.',
      transactionId: 'Transaction ID',
      date: 'Date',
      allLabel: 'All',
      completedLabel: 'Completed',
      activeLabel: 'Active',
      amount: 'Amount',
      status: 'Status',
      reason: 'Reason',
      learner: 'Learner',
      errorModalTitle: 'Request failed',
      submitLabel: 'Dismiss',
    },
  };

</script>

<style lang="scss" scoped>

  .move-down {
    position: relative;
    margin-top: 24px;
  }
  .svg-item {
    margin-right: 12px;
    margin-bottom: -4px;
    font-size: 24px;
  }

</style>
