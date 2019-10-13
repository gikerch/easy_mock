<template>
  <div class="em-mock-expand">
    <h2>Method</h2>
    <p>{{mock.method}}</p>
    <h2>URL</h2>
    <p>{{mock.url}}</p>
    <h2>{{$t('p.detail.expand.description')}}</h2>
    <p>{{mock.description}}</p>
    <Tabs value="request" v-if="mock.parameters || mock.response_model">
      <Tab-pane :label="$t('p.detail.expand.tab[0]')" name="request" v-if="mock.parameters">
        <Table :columns="columnsRequest" :data="request"></Table>
      </Tab-pane>
      <Tab-pane :label="$t('p.detail.expand.tab[1]')" name="response" v-if="mock.response_model">
        <Table :columns="columnsResponse" :data="response"></Table>
      </Tab-pane>
      <Tab-pane label="客户端代码" name="client">
        <Collapse>
          <Panel>
            Python Requests
            <div slot="content">
              <p>
                <pre>import requests

url = "https://www.wisers.ai/"
querystring = {"api":"ailab-demo-apilb.wisers.com:8000/rel-ext/wicore/extract_relation"}
payload = "{\"text\":\"2018年6月6日下午，上海壹账通金融科技有限公司副总裁陈烨一行莅临洛阳高新区管委会交流学习，自贸区管委会副主任郭卫东，高新区金融监管与服务局局长王玉晓共同会见了陈烨一行。\"}"
headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'connection': "keep-alive",
    'content-length': "425",
    'content-type': "application/json",
    'cookie': "pll_language=zh-hk; ROUTEID=.corp-myweb01; _ga=GA1.2.336027509.1570607214; _gid=GA1.2.14128610.1570607214",
    'host': "www.wisers.ai",
    'origin': "https://www.wisers.ai",
    'referer': "https://www.wisers.ai/zh-cn/browse/relation-extraction/demo/",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "dc47d5a8-dbc9-2fee-fa39-7e33c90953ee"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
print(response.text)</pre>
              </p>
            </div>
          </Panel>
          <Panel>
            cURL
            <div slot="content">
              <p>
                <pre>curl -X POST "https://generator3.swagger.io/api/generate" -H "accept: application/octet-stream"</pre>
              </p>
            </div>
          </Panel>
          <Panel>
            Go
            <div slot="content">
              <p>
                <pre>功能开发中</pre>
              </p>
            </div>
          </Panel>
        </Collapse>
      </Tab-pane>
      <Tab-pane label="Class Model" name="class" v-if="mock.response_model && entities.js.length">
        <Collapse>
          <Panel>
            JavaScript
            <div slot="content">
              <p v-for="(item, i) in entities.js" :key="i">
                <pre>{{item}}</pre>
              </p>
            </div>
          </Panel>
          <Panel>
            Objective-C
            <div slot="content">
              <p v-for="(item, i) in entities.oc" :key="i">
                <pre>{{item}}</pre>
              </p>
            </div>
          </Panel>
        </Collapse>
      </Tab-pane>
    </Tabs>
  </div>
</template>

<script>
import {
  getJavaScriptEntities,
  getObjectiveCEntities
} from 'swagger-parser-mock/lib/entity'
import jsBeautify from 'js-beautify/js/lib/beautify'
import DataTypeExpand from './data-type-expand'

export default {
  props: {
    mock: {}
  },
  data () {
    return {
      columnsRequest: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => h(DataTypeExpand, { props: { data: params.row.parameter } })
        },
        { title: this.$t('p.detail.expand.columnsRequest[0]'), key: 'name' },
        { title: this.$t('p.detail.expand.columnsRequest[1]'), key: 'description' },
        { title: this.$t('p.detail.expand.columnsRequest[2]'), key: 'paramType' },
        { title: this.$t('p.detail.expand.columnsRequest[3]'), key: 'dataType' }
      ],
      columnsResponse: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => h(DataTypeExpand, { props: { data: params.row.response } })
        },
        { title: this.$t('p.detail.expand.columnsResponse[0]'), key: 'code' },
        { title: this.$t('p.detail.expand.columnsResponse[1]'), key: 'message' }
      ]
    }
  },
  computed: {
    request () {
      const parameters = this.mock.parameters ? JSON.parse(this.mock.parameters) : []
      return parameters.map(parameter => ({
        name: parameter.name,
        description: parameter.description || this.$t('p.detail.expand.defaultDescription'),
        paramType: parameter.in,
        dataType: this.getParamDataType(parameter),
        parameter: parameter
      }))
    },
    response () {
      const responseModel = this.mock.response_model ? JSON.parse(this.mock.response_model) : {}
      return Object.keys(responseModel).map(code => {
        const response = responseModel[code]
        return {
          code: code,
          message: response.message || response.description || this.$t('p.detail.expand.defaultDescription'),
          response: response
        }
      })
    },
    entities () {
      const res = this.response.filter(o => {
        const code = o.code.toString()
        return code === '200' || code === 'default'
      })[0]
      const response = res ? res.response : {}

      return {
        js: getJavaScriptEntities(response).map(o => jsBeautify.js_beautify(o, { indent_size: 2 })),
        oc: getObjectiveCEntities(response)
      }
    }
  },
  methods: {
    getParamDataType (parameter) {
      const { type, schema } = parameter
      if (type) return type
      if (schema && schema.type) {
        return schema.type === 'array' ? schema.items.type : schema.type
      }
    }
  }
}
</script>
