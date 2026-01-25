const { initializeDB } = require('./models/database');
const path = require('path');

async function main() {
  try {
    console.log('正在初始化数据库...');
    console.log('当前工作目录:', process.cwd());
    
    // 确保 data 目录存在
    const dataDir = path.join(process.cwd(), 'src/data');
    const fs = require('fs');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
      console.log('创建 data 目录:', dataDir);
    }
    
    await initializeDB();
    console.log('数据库初始化完成！');
    process.exit(0);
  } catch (error) {
    console.error('数据库初始化失败:', error);
    process.exit(1);
  }
}

main();
