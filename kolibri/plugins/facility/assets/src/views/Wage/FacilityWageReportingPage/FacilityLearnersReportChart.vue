<template>

  <div>
    <KPageContainer class="container">

      <h2> {{ $tr('headerTitle') }}</h2>  
      <p> {{ $tr('subHeaderText') }}</p>

      <KGrid gutter="16" :debug="false">
        <KGridItem :layout12="{ span: 4 }" />
        <KGridItem :layout12="{ span: 3 }">
          From: <Datepicker v-model="startDate" placeholder="Select Start Date" class="startDate" />

        </KGridItem>
        <KGridItem :layout12="{ span: 3 }">
          To:
          <Datepicker v-model="endDate" placeholder="Select Start Date" />

        </KGridItem>
        <KGridItem :layout12="{ span: 2 }">
          <KButton :primary="true" text="Go" appearance="raised-button" class="move-down" @click="filterByDateRange" />
        </KGridItem>


      </KGrid>

      <PaginatedListContainer
        :items="filterTransactionByStatus"
        :itemsPerPage="10"
        :filterPlaceholder="$tr('searchboxPlaceholderText')"
      >
        <template #otherFilter>
          <KSelect
            v-model="reasonFilter"
            label="Reason"
            :options="listOfReason"
            :inline="true"
            class="type-filter"
          />
        </template>
        <template #default="{ items }">
          <CoreTable
            :selectable="true"
            :emptyMessage="$tr('searchNoResultText')"
            class="move-down"
          >
            <template #headers>
              <th class="table-header">
                {{ $tr('transactionIdLabel') }}
              </th>
              <th class="table-header">
                {{ $tr('learnerLabel') }}
              </th>
              <th class="table-header">
                {{ $tr('dateLabel') }}
              </th>
              <th class="table-header">
                {{ $tr('reasonLabel') }}
              </th>
              <th class="table-header">
                {{ $tr('depositLabel') }}
              </th>
              <th class="table-header">
                {{ $tr('withdrawalLabel') }}
              </th>
              <th class="table-header">
                {{ $tr('afterBalanceLabel') }}
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
                    <span v-if="txn.request_type === 'CREDIT'">{{ txn.transaction_amount }}</span>
                  </td>
                  <td class="table-data">
                    <span v-if="txn.request_type === 'DEBIT'">{{ txn.transaction_amount }}</span>
                  </td>
                  <td class="table-data">
                    {{ txn.after_balance }}
                  </td>

                </tr>
              </tbody>
            </template>       

          </CoreTable>
        </template>
      </PaginatedListContainer>  



    </KPageContainer>
  </div>

</template>


<script>

  import { mapState } from 'vuex';
  import Datepicker from 'vuejs-datepicker';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import PaginatedListContainer from 'kolibri.coreVue.components.PaginatedListContainer';
  import { WageRequestOptions } from 'kolibri.coreVue.vuex.constants';

  export default {
    name: 'FacilityLearnersReportChart',
    components: { PaginatedListContainer, CoreTable, Datepicker },
    mixins: [],
    computed: {
      ...mapState('wage', ['facilityAllLearnersRequests', 'defaultStartDate', 'defaultEndDate']),
      startDateFormatted() {
        return this.formatDate(this.start);
      },
      filterTransactionByStatus() {
        if (this.reasonFilter.value === 'All') {
          return this.transactions;
        }
        return this.transactions.filter(item => item['reason'] === this.reasonFilter.value);
      },
    },
    watch: {
      facilityAllLearnersRequests(requests, oldRequests) {
        this.transactions = this.facilityAllLearnersRequests;
      },
    },
    beforeMount() {
      this.init();
    },
    data() {
      return {
        startDate: null,
        endDate: null,
        reasonFilter: null,
        listOfReason: [
          {
            label: 'All',
            value: 'All',
          },
        ],
        transactions: [],
      };
    },
    methods: {
      init() {
        this.startDate = new Date(this.defaultStartDate);
        this.endDate = new Date(this.defaultEndDate);
        this.transactions = this.facilityAllLearnersRequests;
        let creditOptions = Object.values(WageRequestOptions.CREDIT);
        let debitOptions = Object.values(WageRequestOptions.DEBIT);
        let reasons = creditOptions.concat(debitOptions);
        this.listOfReason = this.listOfReason.concat(reasons);
        this.reasonFilter = this.listOfReason[0];
      },
      toolKitReference(id) {
        return 'icon__' + id;
      },

      formatDate(date) {
        if (date === null) {
          return '';
        }
        let year = date.getFullYear();
        let month = date.getMonth() + 1;
        let day = date.getDate();
        let str = year + '-' + month + '-' + day;
        return str;
      },
      filterByDateRange() {
        let startingDate = this.formatDate(this.startDate);
        let endingDate = this.formatDate(this.endDate);
        this.$store
          .dispatch('wage/getTransactionsByDateRange', {
            startDate: startingDate,
            endDate: endingDate,
            facilityId: this.$store.getters.activeFacilityId,
          })
          .then(transactions => {
            this.$store.commit('wage/UPDATE_LEARNERS_CHART_WAGE_DETAILS', {
              facilityAllWageRequests: transactions,
            });
          })
          .catch(err => {
            this.$store.dispatch('handleApiError', err);
          });
      },
    },
    $trs: {
      headerTitle: "Students' reports",
      subHeaderText: 'Details regarding transactions made by students',
      searchNoResultText: 'No matching transaction found',
      searchboxPlaceholderText: 'Search for student',
      reasonLabel: 'Reason',
      depositLabel: 'Deposit',
      withdrawalLabel: 'Withdrawal',
      dateFilterFrom: 'From:',
      dateFilterTo: 'To:',
      dateLabel: 'Date',
      learnerLabel: 'Student',
      transactionIdLabel: 'Txn ID',
      dateFilterButton: 'Go',
      totalLabel: 'Total',
      afterBalanceLabel: 'Balance',
    },
  };

</script>


<style lang="scss" >

  .move-down {
    position: relative;
    margin-top: 16px;
  }
  .container {
    min-height: 500px;
  }

  .total {
    font-weight: bold;
  }

  .table-header {
    padding: 24px 0;
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

</style>1
