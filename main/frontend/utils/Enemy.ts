/**
 * 敌机类
 *
 * 功能：
 * 1. 三种类型的敌机（小型、中型、大型）
 * 2. 从画布顶部随机位置生成
 * 3. 垂直向下移动
 * 4. 不同类型有不同的速度和分数
 */

import { GameObject } from './GameObject';

export enum EnemyType {
  SMALL = 'small',   // 小型敌机：速度快，分数 10
  MEDIUM = 'medium', // 中型敌机：速度中等，分数 20
  LARGE = 'large',   // 大型敌机：速度慢，分数 50
}

interface EnemyConfig {
  width: number;
  height: number;
  speed: number;
  score: number;
  color: string;
}

const ENEMY_CONFIGS: Record<EnemyType, EnemyConfig> = {
  [EnemyType.SMALL]: {
    width: 30,
    height: 30,
    speed: 3,
    score: 10,
    color: '#FF6B6B', // 红色
  },
  [EnemyType.MEDIUM]: {
    width: 45,
    height: 45,
    speed: 2,
    score: 20,
    color: '#FFA500', // 橙色
  },
  [EnemyType.LARGE]: {
    width: 60,
    height: 60,
    speed: 1,
    score: 50,
    color: '#9B59B6', // 紫色
  },
};

export class Enemy extends GameObject {
  type: EnemyType;
  score: number;

  constructor(type: EnemyType, x: number, y: number = -60) {
    const config = ENEMY_CONFIGS[type];

    super({
      x,
      y,
      width: config.width,
      height: config.height,
      speedX: 0,
      speedY: config.speed,
      color: config.color,
    });

    this.type = type;
    this.score = config.score;
  }

  /**
   * 创建随机类型的敌机
   */
  static createRandom(canvasWidth: number): Enemy {
    // 随机选择敌机类型
    const types = [EnemyType.SMALL, EnemyType.MEDIUM, EnemyType.LARGE];
    const weights = [0.5, 0.3, 0.2]; // 小型敌机出现概率最高
    const random = Math.random();
    let type: EnemyType;

    if (random < weights[0]) {
      type = EnemyType.SMALL;
    } else if (random < weights[0] + weights[1]) {
      type = EnemyType.MEDIUM;
    } else {
      type = EnemyType.LARGE;
    }

    const config = ENEMY_CONFIGS[type];
    // 随机 X 坐标（确保敌机完全在画布内）
    const x = Math.random() * (canvasWidth - config.width);

    return new Enemy(type, x);
  }

  /**
   * 渲染敌机（倒三角形 + 机翼）
   */
  render(ctx: CanvasRenderingContext2D): void {
    const centerX = this.x + this.width / 2;
    const centerY = this.y + this.height / 2;

    // 绘制敌机主体（倒三角形）
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(centerX, this.y + this.height); // 底部顶点
    ctx.lineTo(this.x, this.y); // 左上角
    ctx.lineTo(this.x + this.width, this.y); // 右上角
    ctx.closePath();
    ctx.fill();

    // 绘制机翼（两个小矩形）
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x - 5, centerY - 5, 10, 10); // 左机翼
    ctx.fillRect(this.x + this.width - 5, centerY - 5, 10, 10); // 右机翼

    // 绘制敌机标识（红色圆点）
    ctx.fillStyle = '#FF0000';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fill();
  }

  /**
   * 检查敌机是否飞出画布底部
   */
  isOutOfBounds(canvasHeight: number): boolean {
    return this.y > canvasHeight;
  }
}
