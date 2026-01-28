4.5 聊天接口（/chat SSE，新协议）

POST /chat（SSE 流式）

入参：

{
"conversation_id": "uuid|null",
"user_input": "string",
"user_role": "patient|doctor",
"use_model": "string",
"use_prompt": "string"
}

数据流格式（每条推送均为 JSON 行）：

data: {
"event": "start|ping|delta|tool|final|error",
"conversation_id": "",
"request_id": "",
"data": {}
}

event=tool 的统一结构：

{
"event": "tool",
"conversation_id": "...",
"request_id": "...",
"data": {
"tool_name": "digital_doctor_reasoning|evidence_conclusion|personalized_analysis|integrated_reasoning",
"tool_output": {}
}
}

digital_doctor_reasoning、evidence_conclusion、evidence_conclusion、personalized_analysis：

diagnosis -list：item、file_list [file_name、file_id]

exams-list：item、file_list [file_name、file_id]

treatments-list：item、file_list [file_name、file_id]

evidence_conclusion

evidence_list: file_name、file_id、file_url、file_type

personalized_analysis

record_list: record_id、record_time、record_content

```json
// 类型各举例了一个

// 错误情况
{
    "event": "start",  // 传输开始标志
    "conversation_id": "17591638-4531-477d-b8b9-7596c5cc28c4",
    "request_id": "780634bc-d2be-4abc-9afd-5ff090dceb40",
    "data": null
}，
{
    "event": "error",
    "conversation_id": "17591638-4531-477d-b8b9-7596c5cc28c4",
    "request_id": "780634bc-d2be-4abc-9afd-5ff090dceb40",
    "data": null
}
// 正常情况
{
    "event": "start",  // 传输开始标志
    "conversation_id": "17591638-4531-477d-b8b9-7596c5cc28c4",
    "request_id": "780634bc-d2be-4abc-9afd-5ff090dceb40",
    "data": null
},
{
    "event": "delta",
    "conversation_id": "231eef12-5253-461e-ae35-60a49e7f4fec",
    "request_id": "2c18eece-c3ae-4ede-aed8-cddb34abc50e",
    "data": {
        "content": "",
        "thinking_content": "首先，",
        "tool_calls": null
    }
},
{
    "event": "delta",
    "conversation_id": "231eef12-5253-461e-ae35-60a49e7f4fec",
    "request_id": "2c18eece-c3ae-4ede-aed8-cddb34abc50e",
    "data": {
        "content": "",
        "thinking_content": "用户说：\"这",
        "tool_calls": null
    }
},
{
    "event": "delta",
    "conversation_id": "231eef12-5253-461e-ae35-60a49e7f4fec",
    "request_id": "2c18eece-c3ae-4ede-aed8-cddb34abc50e",
    "data": {
        "content": "",
        "thinking_content": "是我的影像检查图片，我不知道是哪里痛，需要你分析\"。用户处于PATIENTMODE，意味着用户是患者。",
        "tool_calls": null
    }
},
{
    "event": "delta",
    "conversation_id": "231eef12-5253-461e-ae35-60a49e7f4fec",
    "request_id": "2c18eece-c3ae-4ede-aed8-cddb34abc50e",
    "data": {
        "content": "我无法查看图片，",
        "thinking_content": "",
        "tool_calls": null
    }
},
{
    "event": "delta",
    "conversation_id": "231eef12-5253-461e-ae35-60a49e7f4fec",
    "request_id": "2c18eece-c3ae-4ede-aed8-cddb34abc50e",
    "data": {
        "content": "只能基于文本描述。",
        "thinking_content": "",
        "tool_calls": null
    }
},
{
    "event": "final",
    "conversation_id": "17591638-4531-477d-b8b9-7596c5cc28c4",
    "request_id": "780634bc-d2be-4abc-9afd-5ff090dceb40",
    "data": {
        "result_type": "text",
        "text": ""
    }
}

// 特殊操作时候
// {
//     "event": "final",
//     "conversation_id": "5941e7bc-9d48-4dcf-b8a1-b3c4a387100f",
//     "request_id": "7826fc08-29dd-4575-b4b7-c6cd9274891e",
//      "visit_id": "cb67a40d-58ac-44cb-805f-7580d12887a9",
//     "data": {
//          "tool_name": "evidence_conclusion",
//          "tool_output": {
//             "evidence_list": [
//                 {
//                     "file_name": "CT_scan_001.jpg",
//                     "file_id": "file_12345",
//                     "file_url": "https://example.com/files/CT_scan_001.jpg",
//                     "file_type": "image/jpeg"
//                 },
//                 {
//                     "file_name": "blood_test.pdf",
//                     "file_id": "file_67890",
//                     "file_url": "https://example.com/files/blood_test.pdf",
//                     "file_type": "application/pdf"
//                 }
//             ]
//          }
//         }
// }

```
