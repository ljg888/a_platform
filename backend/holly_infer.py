import sys
import os
import time
from datetime import datetime

def generate_html_report(config_id, project, model_path, dataset_path):
    # 创建项目结果目录
    results_dir = os.path.join('results', project)
    os.makedirs(results_dir, exist_ok=True)
    
    # 生成时间戳格式的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(results_dir, f'{timestamp}.html')
    
    # 获取开始时间
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 模拟测试过程
    time.sleep(5)  # 模拟5秒的测试时间
    
    # 获取结束时间
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成HTML内容
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试报告 - {project}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            .report-info {{ margin: 20px 0; }}
            .info-item {{ margin: 10px 0; }}
            .info-label {{ font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>测试报告</h1>
        <div class="report-info">
            <div class="info-item">
                <span class="info-label">配置ID:</span> {config_id}
            </div>
            <div class="info-item">
                <span class="info-label">项目名称:</span> {project}
            </div>
            <div class="info-item">
                <span class="info-label">模型路径:</span> {model_path}
            </div>
            <div class="info-item">
                <span class="info-label">测试集路径:</span> {dataset_path}
            </div>
            <div class="info-item">
                <span class="info-label">开始时间:</span> {start_time}
            </div>
            <div class="info-item">
                <span class="info-label">结束时间:</span> {end_time}
            </div>
        </div>
    </body>
    </html>
    '''
    
    # 写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python holly_infer.py <config_id> <project> <model_path> <dataset_path>")
        sys.exit(1)
        
    config_id = sys.argv[1]
    project = sys.argv[2]
    model_path = sys.argv[3]
    dataset_path = sys.argv[4]
    
    generate_html_report(config_id, project, model_path, dataset_path)
