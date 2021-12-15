<template>

  <KPageContainer>
    <KGrid>
      <KGridItem
        :layout8="{ span: 4 }"
        :layout12="{ span: 6 }"
      >
        <h2>{{ $tr('learnerRequestsLabel') }}</h2>
        <p> {{ $tr('learnerRequestsSubheader') }} </p>
      </KGridItem>
    </KGrid>
    <div v-if="hasTransactions">
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
              <th class="table-checkbox-header">
              </th>
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
                {{ $tr('requestType') }}
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
                    <KCheckbox
                      @change="toggleSelection(txn.id)"
                    />
                  </td>
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
                    {{ txn.status }}
                  </td>


                </tr>
              </tbody>
            </template>  
          </CoreTable>
        </template>
      </PaginatedListContainer>  
      <div class="button-col">
        <span class="message"> {{ selectedMessage }} </span>
        <KButtonGroup>
          <KButton
            :secondary="true"
            appearance="raised-button"
            text="Deny"
            :disabled="buttonsDisabled"
            @click="updateTransactionStatus('false')"
          />
          <KButton
            :primary="true"
            appearance="raised-button"
            text="Approve"
            :disabled="buttonsDisabled"
            @click="updateTransactionStatus('true')"
          />
        </KButtonGroup>
      </div>
    </div>
    <div v-else>
      {{ $tr('noRequests') }}
    </div>
  </KPageContainer>

</template>


<script>

  import { mapState } from 'vuex';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import {
    WageStatusesDropdownOptions,
    DefaultSelectedWageTxnStatus,
  } from 'kolibri.coreVue.vuex.constants';
  import PaginatedListContainer from 'kolibri.coreVue.components.PaginatedListContainer';
  import filterTransactionsByStatusType from 'kolibri.utils.filterTransactionsByStatusType';

  export default {
    name: 'CoachLearnerRequestsBlock',
    components: { PaginatedListContainer, CoreTable },
    mixins: [commonCoreStrings],
    data() {
      return {
        selectedTransactions: {},
        listOfStatuses: [],
        transactions: [],
        statusFilter: null,
        hasTransactions: false,
      };
    },
    computed: {
      ...mapState('wage', ['coachWageRequests']),
      filterTransactionByStatus() {
        return filterTransactionsByStatusType(this.transactions, this.statusFilter.value);
      },
      buttonsDisabled() {
        return Object.keys(this.selectedTransactions).length === 0;
      },
      selectedMessage() {
        const count = Object.keys(this.selectedTransactions).length;
        return this.$tr('learnersSelectedMessage', { count: count });
      },
    },
    watch: {
      coachWageRequests(requests, oldRequests) {
        this.setupData();
      },
    },
    beforeMount() {
      this.init();
    },
    methods: {
      toggleSelection(transactionId) {
        if (transactionId in this.selectedTransactions) {
          this.$delete(this.selectedTransactions, transactionId);
        } else {
          this.$set(
            this.selectedTransactions,
            transactionId,
            this.getTransactionById(transactionId)
          );
        }
      },
      getTransactionById(transactionId) {
        for (var i in this.transactions) {
          if (this.transactions[i].id == transactionId) {
            return this.transactions[i];
          }
        }
      },
      init() {
        this.listOfStatuses = Object.values(WageStatusesDropdownOptions);
        this.statusFilter = DefaultSelectedWageTxnStatus;
        this.setupData();
        this.hasTransactions = Object.keys(this.transactions).length > 0;
      },
      setupData() {
        this.transactions = this.coachWageRequests.filter(
          item =>
            item['coach_approver_id'] === this.$store.getters.currentUserId &&
            item['status'] === 'CREATED'
        );
        this.transactions = this.transactions.sort((a, b) => (a.id < b.id ? 1 : -1));
      },

      toolKitReference(id) {
        return 'icon__' + id;
      },
      updateTransactionStatus(isApproved) {
        const status = isApproved === 'true' ? 'COACH_APPROVED' : 'COACH_DENIED';
        let request = Object.values(this.selectedTransactions);

        request.forEach(item => {
          item['status'] = status;
          item['coach_approver_id'] = this.$store.getters.currentUserId;
          item['coach_approver_name'] = this.$store.getters.currentUserFullname;
        });

        let updatedIds = Object.keys(this.selectedTransactions);
        console.log(updatedIds);

        this.$store
          .dispatch('wage/updateWageTransactionRequest', {
            data: request,
            classId: this.$store.state.classSummary.id,
          })
          .then(response => {
            this.showSnackbarNotification('wageTxnUpdatedSuccessMessage');

            this.$store.commit('wage/UPDATE_COACH_WAGE_REQUEST_LIST', {
              data: updatedIds,
              add: false,
            });
            this.selectedTransactions = {};
          })
          .catch(error => {
            this.$store.dispatch('handleApiError', error);
          });
      },
    },
    $trs: {
      learnerRequestsLabel: "Student's requests",
      learnerRequestsSubheader: 'Requests raised by students requiring your review',
      noRequests: "You don't have any requests.",
      searchboxPlaceholderText: 'Search for transactions..',
      searchNoResultText: 'No matching transactions found.',
      allLabel: 'All',
      completedLabel: 'Completed',
      activeLabel: 'Active',
      transactionId: 'ID',
      date: 'Date',
      amount: 'Amount',
      status: 'Status',
      reason: 'Reason',
      requestType: 'Type',
      learner: 'Learner',
      learnersSelectedMessage:
        '{count, number} {count, plural, one {student} other {students}} selected',
    },
  };

</script>


<style lang="scss" scoped>

  .table-header {
    padding: 24px 0;
  }

  .table-checkbox-header {
    padding: 8px;
  }

  .table-data {
    padding-top: 6px;
    vertical-align: middle;
  }

  .button-col {
    padding: 4px;
    padding-top: 24px;
    text-align: right;
  }

  .svg-item {
    margin-right: 12px;
    margin-bottom: -4px;
    font-size: 24px;
  }

</style>