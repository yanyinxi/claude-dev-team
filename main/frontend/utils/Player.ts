/**
 * 玩家飞机类
 *
 * 功能：
 * 1. 控制玩家飞机的移动（键盘方向键或鼠标）
 * 2. 限制飞机在画布边界内移动
 * 3. 渲染玩家飞机（蓝色三角形）
 */

import { GameObject } from './GameObject';

export class Player extends GameObject {
  private canvasWidth: number;
  private canvasHeight: number;
  private moveSpeed: number = 5; // 移动速度：5像素/帧

  constructor(canvasWidth: number, canvasHeight: number) {
    // 玩家飞机初始位置：画布底部中央
    const width = 60;
    const height = 60;
    const x = (canvasWidth - width) / 2;
    const y = canvasHeight - height - 20;

    super({
      x,
      y,
      width,
      height,
      speedX: 0,
      speedY: 0,
      color: '#4A90E2', // 蓝色
    });

    this.canvasWidth = canvasWidth;
    this.canvasHeight = canvasHeight;
  }

  /**
   * 向左移动
   */
  moveLeft(): void {
    this.x -= this.moveSpeed;
    this.clampPosition();
  }

  /**
   * 向右移动
   */
  moveRight(): void {
    this.x += this.moveSpeed;
    this.clampPosition();
  }

  /**
   * 移动到指定 X 坐标（鼠标控制）
   */
  moveTo(targetX: number): void {
    this.x = targetX - this.width / 2;
    this.clampPosition();
  }

  /**
   * 限制飞机在画布边界内
   */
  private clampPosition(): void {
    if (this.x < 0) {
      this.x = 0;
    }
    if (this.x + this.width > this.canvasWidth) {
      this.x = this.canvasWidth - this.width;
    }
  }

  /**
   * 渲染玩家飞机（蓝色三角形 + 机身）
   */
  render(ctx: CanvasRenderingContext2D): void {
    const centerX = this.x + this.width / 2;
    const centerY = this.y + this.height / 2;

    // 绘制飞机主体（三角形）
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(centerX, this.y); // 顶点
    ctx.lineTo(this.x, this.y + this.height); // 左下角
    ctx.lineTo(this.x + this.width, this.y + this.height); // 右下角
    ctx.closePath();
    ctx.fill();

    // 绘制飞机机身（矩形）
    ctx.fillStyle = '#2E5C8A';
    ctx.fillRect(centerX - 8, centerY, 16, this.height / 2);

    // 绘制飞机窗口（白色圆形）
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.arc(centerX, centerY - 5, 8, 0, Math.PI * 2);
    ctx.fill();
  }

  /**
   * 获取子弹发射位置（飞机顶部中央）
   */
  getBulletSpawnPosition(): { x: number; y: number } {
    return {
      x: this.x + this.width / 2,
      y: this.y,
    };
  }
}
