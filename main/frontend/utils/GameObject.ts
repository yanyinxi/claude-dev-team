/**
 * 游戏对象基类
 *
 * 所有游戏对象（玩家、敌机、子弹）的基类
 * 提供基本的位置、尺寸、速度属性和更新、渲染方法
 */

export interface GameObjectOptions {
  x: number;
  y: number;
  width: number;
  height: number;
  speedX?: number;
  speedY?: number;
  color?: string;
}

export class GameObject {
  x: number;
  y: number;
  width: number;
  height: number;
  speedX: number;
  speedY: number;
  color: string;
  isAlive: boolean;

  constructor(options: GameObjectOptions) {
    this.x = options.x;
    this.y = options.y;
    this.width = options.width;
    this.height = options.height;
    this.speedX = options.speedX || 0;
    this.speedY = options.speedY || 0;
    this.color = options.color || '#000000';
    this.isAlive = true;
  }

  /**
   * 更新游戏对象状态
   * 子类可以重写此方法实现自定义逻辑
   */
  update(): void {
    this.x += this.speedX;
    this.y += this.speedY;
  }

  /**
   * 渲染游戏对象
   * 子类必须重写此方法实现具体渲染逻辑
   */
  render(ctx: CanvasRenderingContext2D): void {
    // 默认渲染为矩形
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
  }

  /**
   * 获取游戏对象的边界框（用于碰撞检测）
   */
  getBounds() {
    return {
      left: this.x,
      right: this.x + this.width,
      top: this.y,
      bottom: this.y + this.height,
    };
  }

  /**
   * 销毁游戏对象
   */
  destroy(): void {
    this.isAlive = false;
  }
}
