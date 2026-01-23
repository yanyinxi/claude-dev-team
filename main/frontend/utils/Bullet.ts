/**
 * 子弹类
 *
 * 功能：
 * 1. 从玩家飞机顶部发射
 * 2. 垂直向上移动
 * 3. 渲染为黄色椭圆形子弹
 */

import { GameObject } from './GameObject';

export class Bullet extends GameObject {
  constructor(x: number, y: number) {
    super({
      x: x - 4, // 子弹宽度的一半，使其居中
      y: y - 16, // 子弹高度
      width: 8,
      height: 16,
      speedX: 0,
      speedY: -8, // 向上移动，速度 8 像素/帧
      color: '#FFD700', // 金黄色
    });
  }

  /**
   * 渲染子弹（黄色椭圆形）
   */
  render(ctx: CanvasRenderingContext2D): void {
    const centerX = this.x + this.width / 2;
    const centerY = this.y + this.height / 2;

    // 绘制子弹主体（椭圆形）
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.ellipse(centerX, centerY, this.width / 2, this.height / 2, 0, 0, Math.PI * 2);
    ctx.fill();

    // 绘制子弹高光（白色小椭圆）
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.ellipse(centerX - 1, centerY - 3, 2, 4, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  /**
   * 检查子弹是否飞出画布顶部
   */
  isOutOfBounds(): boolean {
    return this.y + this.height < 0;
  }
}
