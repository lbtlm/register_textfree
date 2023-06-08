from db.models import BasicConfig

init_base_config = BasicConfig(
    proxy_file="请选择代理池文件",
    email_file="请选择邮箱文件",
    two_fa="abc123456",
    thread_amount=3,
    ie_style="谷歌浏览器"
)
