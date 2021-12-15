<template>

  <div>
    <KPageContainer>
      <KGrid>
        <KGridItem
          :layout8="{ span: 4 }"
          :layout12="{ span: 6 }"
        >
          <h2>{{ $tr('wageDetails') }}</h2>
          <p> {{ currentBalance }} </p>
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

    </KPageContainer>
    <KPageContainer>

      <KGrid>
        <KGridItem
          :layout8="{ span: 4 }"
          :layout12="{ span: 6 }"
        >
          <h2>{{ $tr('wageTransactionDetails') }}</h2>
          <p> {{ $tr('wagerTransactionSubheader') }}</p>
        </KGridItem>
      </KGrid>

      <PaginatedListContainer
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
                {{ $tr('date') }}
              </th>
              <th class="table-header">
                {{ $tr('requestType') }}
              </th>
              <th class="table-header">
                {{ $tr('amount') }}
              </th>

              <th class="table-header">
                {{ $tr('reason') }}
              </th>
              <th class="table-header">
                {{ $tr('coach') }}
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
                    {{ txn.transaction_date }}
                  </td>
                  <td class="table-data">
                    {{ txn.request_type }}
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
                    {{ txn.coach_approver_name }}
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
      <LearnerWageFormModal
        v-if="showCreateFormModal" 
        :supervisors="supervisors" 
        @submit="createWageRequest"
        @cancel="showCreateFormModal = false"
      />
    </KPageContainer>
  </div>

</template>


<script>

  import { mapState } from 'vuex';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import PaginatedListContainer from 'kolibri.coreVue.components.PaginatedListContainer';
  import filterTransactionsByStatusType from 'kolibri.utils.filterTransactionsByStatusType';
  import {
    WageStatusesDropdownOptions,
    DefaultSelectedWageTxnStatus,
  } from 'kolibri.coreVue.vuex.constants';
  import LearnerWageFormModal from './LearnerWageFormModal.vue';

  export default {
    name: 'LearnerWagePage',
    components: { CoreTable, PaginatedListContainer, LearnerWageFormModal },
    mixins: [commonCoreStrings],
    data() {
      return {
        showCreateFormModal: false,
        listOfStatuses: [],
        transactions: [],
        statusFilter: null,
        supervisors: [],
      };
    },
    computed: {
      ...mapState('wage', ['wagedetails']),
      filterTransactionByStatus() {
        return filterTransactionsByStatusType(this.transactions, this.statusFilter.value);
      },
      currentBalance() {
        const amount = this.wagedetails['amount_available'].toString();
        return this.$tr('wageDetailsBalanceLabel', { amount: amount });
      },
    },
    beforeMount() {
      this.init();
    },
    methods: {
      createWageRequest({ amount, requestType, reason, description, supervisor }) {
        this.showCreateFormModal = false;
        this.$store
          .dispatch('wage/createWageTransactionRequest', {
            amount: amount,
            requestType: requestType,
            reason: reason,
            description: description,
            user_id: this.$store.getters.currentUserId,
            user_name: this.$store.getters.currentUserFullname,
            coach_approver_id: supervisor.value,
            coach_approver_name: supervisor.label,
          })
          .then(response => {
            this.showSnackbarNotification('wageTxnCreatedSuccessMessage');
            this.$store.commit('wage/UPDATE_LEARNER_WAGE_DETAILS', response);
            this.transactions.sort((a, b) => (a.id < b.id ? 1 : -1));
          })
          .catch(error => {
            this.$store.dispatch('handleApiError', error);
          });
      },
      init() {
        this.listOfStatuses = Object.values(WageStatusesDropdownOptions);
        this.statusFilter = DefaultSelectedWageTxnStatus;
        this.transactions = this.wagedetails['transactions'].sort((a, b) => (a.id < b.id ? 1 : -1));
        this.supervisors = this.wagedetails['supervisors'];
      },
      toolKitReference(id) {
        return 'icon__' + id;
      },
    },
    $trs: {
      wageDetails: 'Wage account details',
      wageDetailsBalanceLabel: 'Your current balance: {amount}',
      searchboxPlaceholderText: 'Search for transactions..',
      searchNoResultText: 'No matching transactions found.',
      transactionId: 'Txn ID',
      date: 'Date',
      newRequest: 'New Request',
      allLabel: 'All',
      completedLabel: 'Completed',
      activeLabel: 'Active',
      amount: 'Amount',
      status: 'Status',
      requestType: 'Type',
      coach: 'Teacher',
      reason: 'Reason',
      wageTransactionDetails: 'Your transactions',
      wagerTransactionSubheader: 'List of your active and completed requests',
    },
  };

</script>


<style  lang="scss" scoped>

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
