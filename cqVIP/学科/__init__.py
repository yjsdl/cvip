# -*- coding: utf-8 -*-

import re

text = """
<?xml version='1.0'?><?mso-application progid='Excel.Sheet'?>/r/n<Workbook xmlns='urn:schemas-microsoft-com:office:spreadsheet' 
      xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:x='urn:schemas-microsoft-com:office:excel' 
      xmlns:ss='urn:schemas-microsoft-com:office:spreadsheet' xmlns:html='http://www.w3.org/TR/REC-html40'>/r/n<Styles><Style ss:ID='Default' ss:Name='Normal'><Alignment ss:Vertical='Center' ss:Horizontal='Center'/>
      <Borders/><Font ss:FontName='宋体' x:CharSet='134' ss:Size='12'/><Interior/><NumberFormat/><Protection/></Style><Style ss:ID='border'><NumberFormat ss:Format='@'/><Borders>
      <Border ss:Position='Bottom' ss:LineStyle='Continuous' ss:Weight='1'/>
      <Border ss:Position='Left' ss:LineStyle='Continuous' ss:Weight='1'/>
      <Border ss:Position='Right' ss:LineStyle='Continuous' ss:Weight='1'/>
      <Border ss:Position='Top' ss:LineStyle='Continuous' ss:Weight='1'/></Borders></Style></Styles>/r/n<Worksheet ss:Name='Sheet1'>/r/n<Table x:StyleID='border'>/r/n<Row ss:AutoFitHeight='0'><Cell ss:StyleID='border'><Data ss:Type='String'>序  号</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>题　名</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>作　者</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>机　构</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>基  金</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>刊　名</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>年</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>卷</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>期</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>ISSN号</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>C N 号</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>页　码</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>关键词</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>分类号</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>文　摘</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>网　址</Data></Cell>/r/n</Row>/r/n<Row ss:AutoFitHeight='1'><Cell ss:StyleID='border'><Data ss:Type='String'>1</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>新形势下部队健康教育之我见</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>向彩良[1]</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>[1]广州军区联勤部卫生部卫生防疫处</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'></Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>华南国防医学杂志</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>2000</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'></Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>2</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>1009-2595</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>42-1602/R</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>73-74</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>[5872940]健康教育;[5140502]军队;[3908086]卫生教育;国家机器;部队;[6190513]官兵心理;新形势下;</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>R</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>随着人们物资、文化、生活水平的不断提高，追求生命质量的欲望值逐步上升。健康的外延，逐步向生理健康、心理健康和良好的生活、学习、工作环境延伸。因此，军队健康教育的内容也要不断适应社会发展和军队建设需要。新形势下军队健康教育内容应涵盖以下几个方面：
2.1　以防病、治病为主的卫生健康教育
　　继续抓好卫生宣传教育，增强官兵“大卫生观念”。抓好饮食饮水卫生、食品卫生、个人卫生、常见病、传染病、意外伤害防护知识以及劳动卫生、训练伤防治知识教育，并结合各军兵种特点和可能机动作战地域卫生状况和疫情，进行必要的流行病学常识、野营卫生等教育。使官兵掌握必要的防护知识和应急处置技能。
2.2　以家庭、社会和战场为背景的心理健康教育
　　随着时代的发展，军队成员中独生子女的成份含量加大，他们受家庭、社会因素影响较深，习惯自由、浪漫的生活方式，对部队特殊的生活环境、生活方式一时难以适应。部分同志感到生活、工作、学习、训练压力较大，而产生悲观情绪，出现心理障碍。因此，健康教育必须结合官兵心理实际，掌握他们的心理动态，不断了解掌握影响官兵心理变化的原因，突出重点，进行针对性教育。引导他们树立正确的人生观、价值观和奋发向上的精神。帮助他们克服不良影响因素，学会自我调节和防范的方法和措施。不断加强高新技术武器的致伤机理及防护知识学习、训练。使他们对未来战场特征有充分的了解，减少战场恐慌心理因素，使其保持高昂的斗志，良好的心理状态面对战场和突发事件。
2.3　以恶劣环境为背景的生存知识教育
　　未来战争将是全天侯、诸兵种的合成作战，不受地理环境所限。因此健康教育必须充实热带丛林作战、寒带作战、海上作战、登陆作战、高原作战、遭受特殊武器袭击等必要的生存方式教育。使他们掌握寻找水源、食物，辨认方向，识别有毒动植物以及自救互救和遭特殊武器袭击的防护技能等等。从而使官兵在恶劣条件下能很好的生存，并保持有效的战斗力。</Data></Cell><Cell ss:StyleID='border'><Data ss:Type='String'>http://qikan.cqvip.com/Qikan/Article/Detail?id=1001109709</Data></Cell>/r/n</Row>/r/n</Table>/r/n</Worksheet>/r/n</Workbook>
"""

res = re.findall(r'<Row ss:AutoFitHeight=\'1\'>(.*?)</Row>', text)
print(res)