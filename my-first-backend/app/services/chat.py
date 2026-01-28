import asyncio
import json
import uuid
from typing import AsyncGenerator
from app.schemas.chat import (
    ChatRequest,
    SSEEventData,
    DeltaData,
    FinalData,
    ToolData,
    DigitalDoctorReasoningOutput,
    EvidenceConclusionOutput,
    PersonalizedAnalysisOutput,
)


def _generate_mock_digital_doctor_reasoning() -> dict:
    """生成模拟的数字医生推理数据"""
    return {
        "diagnosis": {
            "list": [
                {
                    "item": "疑似肺炎",
                    "file_list": [
                        {
                            "file_name": "CT_scan_001.jpg",
                            "file_id": "file_12345"
                        },
                        {
                            "file_name": "X_ray_chest_001.jpg",
                            "file_id": "file_12346"
                        }
                    ]
                },
                {
                    "item": "支气管炎可能性",
                    "file_list": [
                        {
                            "file_name": "bronchoscopy_report.pdf",
                            "file_id": "file_12347"
                        }
                    ]
                },
                {
                    "item": "上呼吸道感染",
                    "file_list": []
                }
            ]
        },
        "exams": {
            "list": [
                {
                    "item": "血常规检查",
                    "file_list": [
                        {
                            "file_name": "blood_test.pdf",
                            "file_id": "file_67890"
                        }
                    ]
                },
                {
                    "item": "C反应蛋白检查",
                    "file_list": [
                        {
                            "file_name": "crp_test.pdf",
                            "file_id": "file_67891"
                        }
                    ]
                },
                {
                    "item": "胸部CT检查",
                    "file_list": [
                        {
                            "file_name": "CT_scan_001.jpg",
                            "file_id": "file_12345"
                        }
                    ]
                },
                {
                    "item": "痰培养检查",
                    "file_list": [
                        {
                            "file_name": "sputum_culture.pdf",
                            "file_id": "file_67892"
                        }
                    ]
                }
            ]
        },
        "treatments": {
            "list": [
                {
                    "item": "抗生素治疗",
                    "file_list": [
                        {
                            "file_name": "prescription.pdf",
                            "file_id": "file_11111"
                        }
                    ]
                },
                {
                    "item": "对症支持治疗",
                    "file_list": [
                        {
                            "file_name": "supportive_care.pdf",
                            "file_id": "file_11112"
                        }
                    ]
                },
                {
                    "item": "雾化吸入治疗",
                    "file_list": [
                        {
                            "file_name": "nebulization_guide.pdf",
                            "file_id": "file_11113"
                        }
                    ]
                }
            ]
        }
    }


def _generate_mock_evidence_conclusion() -> dict:
    """生成模拟的证据结论数据"""
    return {
        "evidence_list": [
            {
                "file_name": "CT_scan_001.jpg",
                "file_id": "file_12345",
                "file_url": "https://example.com/files/CT_scan_001.jpg",
                "file_type": "image/jpeg"
            },
            {
                "file_name": "X_ray_chest_001.jpg",
                "file_id": "file_12346",
                "file_url": "https://example.com/files/X_ray_chest_001.jpg",
                "file_type": "image/jpeg"
            },
            {
                "file_name": "blood_test.pdf",
                "file_id": "file_67890",
                "file_url": "https://example.com/files/blood_test.pdf",
                "file_type": "application/pdf"
            },
            {
                "file_name": "crp_test.pdf",
                "file_id": "file_67891",
                "file_url": "https://example.com/files/crp_test.pdf",
                "file_type": "application/pdf"
            },
            {
                "file_name": "sputum_culture.pdf",
                "file_id": "file_67892",
                "file_url": "https://example.com/files/sputum_culture.pdf",
                "file_type": "application/pdf"
            },
            {
                "file_name": "prescription.pdf",
                "file_id": "file_11111",
                "file_url": "https://example.com/files/prescription.pdf",
                "file_type": "application/pdf"
            },
            {
                "file_name": "medical_report.pdf",
                "file_id": "file_11114",
                "file_url": "https://example.com/files/medical_report.pdf",
                "file_type": "application/pdf"
            }
        ]
    }


def _generate_mock_personalized_analysis() -> dict:
    """生成模拟的个性化分析数据"""
    return {
        "record_list": [
            {
                "record_id": "record_001",
                "record_time": "2024-01-15T10:30:00Z",
                "record_content": "患者主诉：胸痛3天，伴有咳嗽，无发热，无呼吸困难。疼痛性质为钝痛，活动后加重。"
            },
            {
                "record_id": "record_002",
                "record_time": "2024-01-10T14:20:00Z",
                "record_content": "既往病史：高血压病史5年，规律服用降压药物，血压控制良好。无糖尿病、心脏病等慢性疾病史。"
            },
            {
                "record_id": "record_003",
                "record_time": "2024-01-08T09:15:00Z",
                "record_content": "体格检查：体温36.5℃，血压130/80mmHg，心率78次/分，呼吸18次/分。双肺呼吸音清，未闻及干湿性啰音。"
            },
            {
                "record_id": "record_004",
                "record_time": "2024-01-05T11:00:00Z",
                "record_content": "辅助检查：血常规示白细胞计数正常，中性粒细胞比例略高。胸部CT示双肺纹理增粗，未见明显实变影。"
            },
            {
                "record_id": "record_005",
                "record_time": "2024-01-03T16:45:00Z",
                "record_content": "诊断：上呼吸道感染，支气管炎可能性大。建议抗感染治疗，对症支持治疗，注意休息，多饮水。"
            },
            {
                "record_id": "record_006",
                "record_time": "2023-12-28T10:20:00Z",
                "record_content": "用药记录：阿莫西林胶囊0.5g，每日3次，口服；布洛芬缓释胶囊0.3g，每日2次，口服。"
            },
            {
                "record_id": "record_007",
                "record_time": "2023-12-25T14:30:00Z",
                "record_content": "随访记录：患者症状较前好转，咳嗽减轻，胸痛缓解。建议继续当前治疗方案，1周后复查。"
            }
        ]
    }


async def chat_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    """
    聊天流式响应生成器
    
    :param request: 聊天请求
    :yield: SSE 格式的数据行
    """
    conversation_id = request.conversation_id or str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    
    try:
        # 发送 start 事件
        start_event = SSEEventData(
            event="start",
            conversation_id=conversation_id,
            request_id=request_id,
            data=None
        )
        yield f"data: {start_event.model_dump_json()}\n\n"
        await asyncio.sleep(0.1)
        
        # 模拟思考过程（delta 事件）- 增加更多思考内容
        thinking_contents = [
            "首先，我需要分析用户的输入内容。",
            "用户说：\"{}\"。".format(request.user_input),
            "用户处于{}模式，意味着用户是{}。".format(
                request.user_role.upper(),
                "患者" if request.user_role == "patient" else "医生"
            ),
            "根据业务场景 {}，我需要采用相应的处理策略。".format(request.business_scenario),
            "当前使用的模型ID是 {}，提示词ID是 {}。".format(request.model_id, request.prompt_id),
            "让我先理解用户的核心诉求和问题背景。",
            "用户可能面临的问题包括：症状描述不清晰、需要专业建议、或者需要辅助诊断。",
            "我需要结合医疗知识库和临床经验来提供准确的回答。",
            "考虑到用户的角色是{}，回答的深度和专业程度需要适当调整。".format(
                "患者" if request.user_role == "patient" else "医生"
            ),
            "现在开始生成回答内容，确保信息准确、易懂且具有指导意义。"
        ]
        
        for thinking in thinking_contents:
            delta_event = SSEEventData(
                event="delta",
                conversation_id=conversation_id,
                request_id=request_id,
                data=DeltaData(
                    content="",
                    thinking_content=thinking,
                    tool_calls=None
                ).model_dump()
            )
            yield f"data: {delta_event.model_dump_json()}\n\n"
            await asyncio.sleep(0.15)
        
        # 模拟内容生成（delta 事件）- 增加更多详细内容
        content_parts = [
            "感谢您的咨询。",
            "根据您提供的信息，我将为您进行详细的分析和建议。",
            "\n\n",
            "**一、问题分析**\n\n",
            "您提到的问题需要从多个角度进行考虑。",
            "首先，我们需要明确症状的具体表现、持续时间以及可能的诱因。",
            "其次，需要了解您的既往病史、用药情况以及家族病史等相关信息。",
            "最后，结合您的年龄、性别、生活习惯等因素进行综合判断。",
            "\n\n",
            "**二、专业建议**\n\n",
            "基于您的情况，我建议您：",
            "\n1. ",
            "及时就医，进行专业的医学检查。",
            "建议您前往正规医院的相关科室（如内科、外科、专科门诊等）进行详细检查。",
            "\n2. ",
            "完善相关检查项目。",
            "根据您的症状，可能需要进行血常规、尿常规、影像学检查（如X光、CT、MRI等）等检查。",
            "这些检查有助于明确诊断，为后续治疗提供依据。",
            "\n3. ",
            "注意观察症状变化。",
            "在就医前，请密切观察症状的变化情况，包括：",
            "症状的严重程度、发作频率、持续时间、是否有加重或缓解的趋势等。",
            "这些信息对医生的诊断非常有帮助。",
            "\n4. ",
            "保持良好的生活习惯。",
            "在治疗期间，建议您：",
            "保持充足的睡眠，避免熬夜；",
            "饮食清淡，避免辛辣刺激食物；",
            "适当运动，但避免剧烈运动；",
            "保持心情愉悦，避免过度焦虑。",
            "\n\n",
            "**三、注意事项**\n\n",
            "在等待就医或治疗期间，请注意以下几点：",
            "\n- ",
            "不要自行用药，尤其是处方药，应在医生指导下使用。",
            "\n- ",
            "如果症状突然加重或出现新的症状，应立即就医。",
            "\n- ",
            "保持与医生的良好沟通，及时反馈治疗效果和身体反应。",
            "\n- ",
            "定期复查，按照医生的建议进行随访。",
            "\n\n",
            "**四、后续建议**\n\n",
            "建议您建立健康档案，记录症状变化、检查结果、用药情况等信息。",
            "这将有助于医生更好地了解您的病情，制定个性化的治疗方案。",
            "同时，建议您关注相关的健康知识，提高自我保健意识。",
            "\n\n",
            "希望以上信息对您有所帮助。",
            "如果您还有其他问题或需要进一步咨询，请随时告诉我。",
            "祝您早日康复！"
        ]
        
        for content in content_parts:
            delta_event = SSEEventData(
                event="delta",
                conversation_id=conversation_id,
                request_id=request_id,
                data=DeltaData(
                    content=content,
                    thinking_content="",
                    tool_calls=None
                ).model_dump()
            )
            yield f"data: {delta_event.model_dump_json()}\n\n"
            await asyncio.sleep(0.1)
        
        # 根据用户输入决定是否发送 tool 事件
        should_send_tool = "分析" in request.user_input or "检查" in request.user_input
        
        if should_send_tool:
            # 发送 tool 事件（根据场景选择不同的工具）
            tool_name = "evidence_conclusion"  # 可以根据业务逻辑选择
            tool_output = {}
            
            if tool_name == "digital_doctor_reasoning":
                tool_output = _generate_mock_digital_doctor_reasoning()
            elif tool_name == "evidence_conclusion":
                tool_output = _generate_mock_evidence_conclusion()
            elif tool_name == "personalized_analysis":
                tool_output = _generate_mock_personalized_analysis()
            
            tool_event = SSEEventData(
                event="tool",
                conversation_id=conversation_id,
                request_id=request_id,
                data=ToolData(
                    tool_name=tool_name,
                    tool_output=tool_output
                ).model_dump()
            )
            yield f"data: {tool_event.model_dump_json()}\n\n"
            await asyncio.sleep(0.1)
            
            # 发送 final 事件（tool 类型）
            final_event = SSEEventData(
                event="final",
                conversation_id=conversation_id,
                request_id=request_id,
                data=FinalData(
                    result_type="tool",
                    text="",
                    data={
                        "tool_name": tool_name,
                        "tool_output": tool_output
                    }
                ).model_dump()
            )
            yield f"data: {final_event.model_dump_json()}\n\n"
        else:
            # 发送 final 事件（text 类型）- 汇总所有生成的内容
            final_text = (
                "感谢您的咨询。根据您提供的信息，我将为您进行详细的分析和建议。\n\n"
                "**一、问题分析**\n\n"
                "您提到的问题需要从多个角度进行考虑。首先，我们需要明确症状的具体表现、持续时间以及可能的诱因。"
                "其次，需要了解您的既往病史、用药情况以及家族病史等相关信息。"
                "最后，结合您的年龄、性别、生活习惯等因素进行综合判断。\n\n"
                "**二、专业建议**\n\n"
                "基于您的情况，我建议您：\n1. 及时就医，进行专业的医学检查。"
                "建议您前往正规医院的相关科室（如内科、外科、专科门诊等）进行详细检查。\n2. 完善相关检查项目。"
                "根据您的症状，可能需要进行血常规、尿常规、影像学检查（如X光、CT、MRI等）等检查。"
                "这些检查有助于明确诊断，为后续治疗提供依据。\n3. 注意观察症状变化。"
                "在就医前，请密切观察症状的变化情况，包括症状的严重程度、发作频率、持续时间、是否有加重或缓解的趋势等。"
                "这些信息对医生的诊断非常有帮助。\n4. 保持良好的生活习惯。"
                "在治疗期间，建议您保持充足的睡眠，避免熬夜；饮食清淡，避免辛辣刺激食物；"
                "适当运动，但避免剧烈运动；保持心情愉悦，避免过度焦虑。\n\n"
                "**三、注意事项**\n\n"
                "在等待就医或治疗期间，请注意以下几点：\n- 不要自行用药，尤其是处方药，应在医生指导下使用。\n- "
                "如果症状突然加重或出现新的症状，应立即就医。\n- 保持与医生的良好沟通，及时反馈治疗效果和身体反应。\n- "
                "定期复查，按照医生的建议进行随访。\n\n"
                "**四、后续建议**\n\n"
                "建议您建立健康档案，记录症状变化、检查结果、用药情况等信息。"
                "这将有助于医生更好地了解您的病情，制定个性化的治疗方案。"
                "同时，建议您关注相关的健康知识，提高自我保健意识。\n\n"
                "希望以上信息对您有所帮助。如果您还有其他问题或需要进一步咨询，请随时告诉我。祝您早日康复！"
            )
            final_event = SSEEventData(
                event="final",
                conversation_id=conversation_id,
                request_id=request_id,
                data=FinalData(
                    result_type="text",
                    text=final_text
                ).model_dump()
            )
            yield f"data: {final_event.model_dump_json()}\n\n"
            
    except Exception as e:
        # 发送 error 事件
        error_event = SSEEventData(
            event="error",
            conversation_id=conversation_id,
            request_id=request_id,
            data=None
        )
        yield f"data: {error_event.model_dump_json()}\n\n"